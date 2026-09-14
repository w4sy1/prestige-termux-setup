# Użycie

`python app.py --profile developer` — plan.
`python app.py --profile developer --apply` — konfiguracja i instalacja przez pkg.
`python app.py --rollback ~/backup/prestige-IDENTYFIKATOR --apply` — cofnięcie .bashrc.
Na początku potrzebny Python dostępny w Termuxie. Backend `pkg` i dostęp do jego repozytorium.
Profile: minimal/developer/network/security/full.

Nie nadpisuje istniejącej treści .bashrc; dopisuje oznaczony blok tylko raz.
Kopia powstaje przed zmianą. Rollback odmówi nadpisania późniejszych zmian użytkownika.
Instalacja pakietów może się nie udać po zmianie .bashrc; zachowana kopia umożliwia rollback.
Nie uruchamia sshd, nie tworzy kluczy, zmienia tożsamość Git wyłącznie na jawne żądanie.

Rollback nie odinstalowuje pakietów i nie usuwa utworzonych katalogów.

## Rozszerzenia 0.2.0

Opcje `--git-name "Imię Nazwisko" --git-email "adres@example.com"` dopisują tożsamość
użytkownika do .gitconfig. Obie opcje trzeba podać razem. `--ssh-client` dodaje keepalive
klienta SSH. Wszystkie zmieniane pliki są zapisywane w backupie przed pierwszą zmianą.
Rollback obejmuje .bashrc, .gitconfig i .ssh/config, odmawiając nadpisania późniejszych zmian.
Nie tworzy kluczy ani nie uruchamia serwera SSH. Nadal wymagany test na fizycznym Termuxie.
