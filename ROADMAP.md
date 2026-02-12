# 🗺️ Roadmap för Bokklubb-Bot Migrering

## 🎯 Översikt
Migrera bokklubbssystemet från lokal PC till Raspberry Pi med framtida integration av chat-bot (Telegram/Signal/Discord).

## 📋 Fas 1: Grundläggande Migrering (KLAR)
- [x] Överför filer till Raspberry Pi
- [x] Installera Python 3.7 + curl
- [x] Testa synkronisering (`./bookclub -sync`)
- [x] Fixa bash/zsh-kompatibilitet (ändra shebang till `#!/bin/bash`)

## 🔧 Fas 2: Förenkla Pi-versionen
### Mål: Skapa en renodlad Pi-version utan onödiga dependencies
- [ ] Ta bort `-chat` och `-dev` från Pi-skriptet
- [ ] Uppdatera `-setup` för endast nödvändiga dependencies:
  - Python 3.7+
  - curl
  - git (valfritt)
  - INTE `aider-chat`
- [ ] Skapa cron-jobb för regelbunden synkronisering (t.ex. varje dag)
- [ ] Optimera för låg resursanvändning på Pi

### Filändringar:
- Skapa `bookclub.pi` (förenklad version)
- Uppdatera `README.md` med Pi-specifika instruktioner
- Skapa `cron_setup.sh` för automatisk synkronisering

## 🤖 Fas 3: Bot-Integration
### Mål: Möjliggör fjärrstyrning via chat-bot
- [ ] Välj plattform:
  - **Telegram** (enklast, bra dokumentation)
  - **Signal** (mer privat, kräver Signal-Server)
  - **Discord** (bra för communities)
- [ ] Skapa bot-token och konfiguration
- [ ] Implementera webhook/API på Pi:n
- [ ] Lägg till grundläggande kommandon:
  - `/books` - Visa senaste lästa böcker
  - `/reading` - Visa pågående läsning
  - `/recommend` - Få bokrekommendationer baserat på historik
  - `/sync` - Manuell synkronisering
  - `/stats` - Visa lässtatistik

### Tekniskt:
- Använd `python-telegram-bot` eller liknande bibliotek
- Implementera säker autentisering
- Designa enkel REST API om flera klienter behövs

## 🧠 Fas 4: AI/Logik-lager
### Mål: Intelligent bokanalys och rekommendationer
- [ ] Besluta om arkitektur:
  - **Alternativ A:** Lokal AI (lättviktig, privat)
    - Använd enkel ML för rekommendationer
    - Inga externa API-anrop
  - **Alternativ B:** Extern API (mer kraftfull)
    - Använd OpenAI/Anthropic/etc
    - Kräver internetuppkoppling
- [ ] Implementera bokanalys-logik:
  - Analysera genrer från titlar/författare
  - Identifiera läsvanor
  - Generera personliga rekommendationer
- [ ] Lägg till avancerad statistik:
  - Böcker per månad/år
  - Genomsnittligt betyg
  - Mest läste författare

## 🔒 Fas 5: Produktionssäkerhet
### Mål: Gör systemet robust och säkert
- [ ] Implementera autentisering för bot-kommandon
- [ ] Lägg till omfattande felhantering och logging
- [ ] Skapa backup-system för bokloggen
- [ ] Implementera hälsokontroller (health checks)
- [ ] Konfigurera automatiska uppdateringar (säkerhetsuppdateringar)

## 🗂️ Filstruktur (Föreslagen)
```
/bookclub-pi/
├── bookclub.pi                 # Huvudskript (förenklad)
├── sync_books.py              # Synkroniseringslogik
├── bot/                       # Bot-implementation
│   ├── telegram_bot.py
│   ├── commands.py
│   └── config.py
├── api/                       # REST API (om behövs)
│   ├── app.py
│   └── endpoints.py
├── analysis/                  # AI/analys-logik
│   ├── recommender.py
│   └── statistics.py
├── data/                      # Databaser/loggar
│   ├── reading_log.md
│   ├── reading_in_progress.md
│   └── backups/
├── config/                    # Konfiguration
│   ├── .env
│   └── cron_jobs
└── docs/                      # Dokumentation
    ├── SETUP_PI.md
    └── BOT_INTEGRATION.md
```

## ⚙️ Tekniska Krav
### Raspberry Pi (Volumio)
- Python 3.7+
- curl för Goodreads API
- Öppen port för webhook (om extern bot)
- Tillräckligt med diskutrymme för bokloggar

### Bot-plattform
- Internetuppkoppling
- Bot-token/API-nyckel
- Webhook-support (för Telegram/Discord)

## 🚀 Omedelbara Nästa Steg
1. **Testa synkronisering** på Pi:n: `./bookclub -sync`
2. **Skapa förenklad version** av `bookclub` för Pi
3. **Börja med Telegram-bot** (enklaste vägen):
   ```bash
   pip3 install python-telegram-bot
   ```
4. **Implementera enkelt `/books`-kommando**

## 📝 Anteckningar från Nuvarande Session
- Pi:n kör Volumio (Raspbian Buster) med Python 3.7.3
- Användare `volumio` har NOPASSWD sudo för `apt-get`
- `aider-chat` är inte kompatibelt med Python 3.7 (networkx==3.1 kräver Python 3.8+)
- Bash-skript fungerar efter shebang-ändring till `#!/bin/bash`

## 🔗 Resurser
- [python-telegram-bot dokumentation](https://github.com/python-telegram-bot/python-telegram-bot)
- [Goodreads API dokumentation](https://www.goodreads.com/api)
- [Raspberry Pi cron guide](https://www.raspberrypi.com/documentation/computers/os.html#cron)

## 📞 Kontaktpunkt för Nästa Session
- Starta med att testa synkronisering på Pi:n
- Skapa förenklad `bookclub.pi`-version
- Börja implementera Telegram-bot med grundläggande kommandon

---
*Senast uppdaterad: 2026-02-12*
*Status: Pausad - Väntar på nästa session*
````
