# Użycie

`python app.py --profile developer` — plan.
`python app.py --profile developer --apply` — konfiguracja i instalacja przez pkg.
`python app.py --rollback ~/backup/prestige-IDENTYFIKATOR --apply` — cofnięcie .bashrc.
Na początku potrzebny Python dostępny w Termuxie. Backend `pkg` i dostęp do jego repozytorium.
Profile: minimal/developer/network/security/full.

Nie nadpisuje istniejącej treści .bashrc; dopisuje oznaczony blok tylko raz.
Kopia powstaje przed zmianą. Rollback odmówi nadpisania późniejszych zmian użytkownika.
Instalacja pakietów może się nie udać po zmianie .bashrc; zachowana kopia umożliwia rollback.
Nie uruchamia sshd, nie tworzy kluczy, nie zmienia globalnej tożsamości Git.
SSH i Git dostają pakiety, alias Git, ale dalszą konfigurację kont pozostawia użytkownikowi.
Rollback nie odinstalowuje pakietów i nie usuwa utworzonych katalogów.
