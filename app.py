from pathlib import Path
import os
import shutil
import sys
import uuid
from runtime import atomic_json,digest,entry,inside,parser,read_json,run

PROFILES={
 'minimal':['git','python','curl','nano'],
 'developer':['git','python','curl','nano','vim','tmux','jq','zip','unzip'],
 'network':['git','python','curl','wget','openssh','dnsutils','nmap','jq'],
 'security':['git','python','curl','openssh','dnsutils','nmap','jq','openssl'],
}
PROFILES['full']=sorted({p for values in PROFILES.values() for p in values})
FOLDERS=['projects','tools','scripts','logs','backup']
BLOCK='\n# BEGIN PRESTIGE TECH\nexport PATH="$HOME/scripts:$HOME/tools:$PATH"\nalias ll="ls -alF"\nalias py="python"\nalias gs="git status"\n# END PRESTIGE TECH\n'

def configure(home):
    home=Path(home).resolve()
    path=inside(home,'.bashrc')
    original=path.read_text(encoding='utf-8') if path.exists() else None
    if original is not None and '# BEGIN PRESTIGE TECH' in original:
        return {'changed':False,'reason':'Blok Prestige Tech już istnieje.'}
    backup=inside(home,'backup')/('prestige-'+uuid.uuid4().hex)
    backup.mkdir(parents=True,mode=0o700)
    new=(original or '')+BLOCK
    manifest={'file':'.bashrc','original':original,'after_sha256':None}
    atomic_json(backup/'manifest.json',manifest)
    path.write_text(new,encoding='utf-8')
    manifest['after_sha256']=digest(path)
    atomic_json(backup/'manifest.json',manifest)
    for folder in FOLDERS:inside(home,folder).mkdir(exist_ok=True)
    return {'changed':True,'backup':str(backup),'ssh':'Pakiet klienta jest dostępny w wybranych profilach; serwer nie jest uruchamiany.'}

def restore(home,backup):
    home=Path(home).resolve();backup=Path(backup).resolve()
    backup.relative_to(home/'backup')
    data=read_json(backup/'manifest.json')
    if data.get('file')!='.bashrc':raise ValueError('Niedozwolony plik.')
    path=inside(home,'.bashrc')
    if not path.is_file() or digest(path)!=data['after_sha256']:raise ValueError('Konfiguracja zmieniona; rollback odmówiony.')
    if data['original'] is None:path.unlink()
    else:path.write_text(data['original'],encoding='utf-8')
    return {'restored':True,'packages':'Pakiety pozostają zainstalowane; rollback obejmuje .bashrc.'}

def build():
    p=parser('Konfiguracja Termuxa. Domyślnie tylko plan.')
    p.add_argument('--profile',choices=PROFILES,default='minimal')
    p.add_argument('--apply',action='store_true',help='Zainstaluj pakiety i zmień konfigurację')
    p.add_argument('--rollback',help='Katalog kopii konfiguracji')
    return p

def handle(args):
    plan={'packages':PROFILES[args.profile],'folders':FOLDERS,'changes':['Blok PATH i aliasów w .bashrc'],'rollback':args.rollback}
    if not args.apply:return {'dry_run':True,'plan':plan}
    prefix=os.environ.get('PREFIX','')
    if 'com.termux' not in prefix or not shutil.which('pkg'):raise OSError('Wymagany Termux z pkg.')
    home=Path.home()
    if args.rollback:return restore(home,args.rollback)
    result=configure(home)
    run(['pkg','install','-y',*PROFILES[args.profile]],timeout=900)
    return {**result,'packages':PROFILES[args.profile]}

if __name__=='__main__':sys.exit(entry(build,handle))
