from pathlib import Path
import tempfile
import unittest
from configuration import configure,restore,quote_git

class ConfigurationTests(unittest.TestCase):
    def test_git_ssh_backup_restore(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'.gitconfig').write_text('[core]\n editor = vim\n')
            result=configure(root,'Test User','test@example.invalid',True)
            self.assertIn('Test User',(root/'.gitconfig').read_text());self.assertTrue((root/'.ssh/config').exists())
            self.assertFalse(configure(root,'Test User','test@example.invalid',True)['changed'])
            restore(root,result['backup']);self.assertEqual((root/'.gitconfig').read_text(),'[core]\n editor = vim\n');self.assertFalse((root/'.ssh/config').exists())
    def test_validation_before_writes(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):configure(d,'Name',None)
            self.assertEqual(list(Path(d).iterdir()),[])
    def test_git_injection(self):
        with self.assertRaises(ValueError):quote_git('name\n[alias]\n x=!bad')
