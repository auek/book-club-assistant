# 🗺️ Comprehensive Roadmap & Migration Plan för Bokklubb-Bot

## 🎯 Översikt
Denna dokument kombinerar den långsiktiga roadmapen med den detaljerade migrationsplanen till en enda källa för sanning. Planen beskriver progressionen från nuvarande fungerande system till en modulär arkitektur som stödjer både PC och Raspberry Pi, med framtida integration av chat-bot (Telegram/Signal/Discord) och AI-funktionalitet.

## 📋 Nuvarande Status (Baslinje)
Följande fungerar redan och ska bevaras:
- ✅ `./bookclub -sync` fungerar perfekt (använder original `sync_books.py`)
- ✅ `python telegram_bot.py` körs (monolitisk bot)
- ✅ `bookclub.pi` existerar (behöver `chmod +x`)
- ✅ Grundläggande `src/`-struktur finns men saknar implementering

**Implementeringsstatus (uppdaterad 2026-02-13):**
- ✅ **Fas 0** (Förberedelser) är slutförd: behörigheter fixade, kataloger skapade, backup finns.
- ✅ **Fas 1** (Sync-modulen) är slutförd: `src/sync/` moduler skapade, `scripts/sync_books_refactored.py` implementerad och `sync_books.py` ersatt med en wrapper.
- ✅ **Fas 2** (Data-lagret) är slutförd: `src/data/models.py` och `storage.py` implementerade.
- ⚠️ **Fas 3** (Refaktorera Telegram-boten) är påbörjad: Moduler för middleware, core och kommandon skapade.
- ❌ **Fas 4–6** (Launcher, Förbättringar, Testning) är inte påbörjade.

## 🔄 Migreringsfaser – Steg-för-steg

### Fas 0: Förberedelser (Dag 1) – **SLUTFÖRD**
**Mål**: Förbered miljön utan att ändra fungerande kod.

1. **Fixera behörigheter** för `bookclub.pi`:
   ```bash
   chmod +x bookclub.pi
   ```
2. **Skapa tomma `src/`-underkataloger**:
   ```bash
   mkdir -p src/{cli,sync,bot/{commands,middleware},data,utils}
   mkdir -p config/prompts tests/{test_sync,test_bot,test_utils}
   ```
3. **Uppdatera `.gitignore`** för de nya katalogerna
4. **Skapa backup** av nuvarande skript:
   ```bash
   cp sync_books.py sync_books.py.backup
   cp telegram_bot.py telegram_bot.py.backup
   ```

### Fas 1: Extrahera Sync-modulen (Dag 2–3) – **SLUTFÖRD**
**Regel**: Behåll original `sync_books.py` fungerande medan ny modul byggs vid sidan av.

1. ✅ **Skapa `src/sync/fetch.py`** – flytta `curl`/API-logik från `sync_books.py`
2. ✅ **Skapa `src/sync/parse.py`** – flytta `parse_xml()` och `sort_books()`
3. ✅ **Skapa `src/sync/render.py`** – flytta `generate_markdown()` och `cleanup_files()`
4. ✅ **Skapa `scripts/sync_books_refactored.py`** som importerar från `src.sync`
5. ✅ **Testa sida vid sida** för att verifiera identisk utdata
6. ✅ **Ersätt original `sync_books.py`** med en tunn wrapper

### Fas 2: Extrahera Data-lagret (Dag 4) – **SLUTFÖRD**
**Mål**: Isolera fil-I/O och datamodeller.

1. ✅ **Skapa `src/data/models.py`** med `Book`-dataklass
2. ✅ **Skapa `src/data/storage.py`** med funktioner för att läsa/skriva loggfiler
3. ✅ **Uppdatera sync-modulen** att använda dessa datafunktioner
4. ✅ **Testa** att synkroniseringen fortfarande fungerar

### Fas 3: Refaktorera Telegram-boten (Dag 5–7) – **INTE PÅBÖRJAD**
**Känsligaste delen** – boten fungerar redan. Arbeta inkrementellt.

1. ❌ **Skapa `src/bot/core.py`** – flytta `main()`, applikationsbyggare, felhanterare
2. ❌ **Skapa `src/bot/middleware/auth.py`** – flytta `@auth_only`-dekoratorn
3. ❌ **Skapa `src/bot/middleware/formatters.py`** – flytta formateringsfunktioner
4. ❌ **Skapa `src/bot/commands/`** – en fil per kommando (start, help, books, progress, discuss)
5. ❌ **Skapa `scripts/telegram_bot_refactored.py`** som importerar från `src.bot`
6. ❌ **Kör båda botarna temporärt** för att verifiera identiskt beteende
7. ❌ **Ersätt original `telegram_bot.py`** med tunn wrapper när säker

### Fas 4: Uppdatera Launcher-skripten (Dag 8) – **EJ PÅBÖRJAD**
**Mål**: Gör så att `bookclub` och `bookclub.pi` använder de nya modulerna internt.

1. ❌ **Skapa `src/cli/sync_cli.py`** – funktion som efterliknar `-sync`-grenen av `bookclub`
2. ❌ **Skapa `src/cli/bot_cli.py`** – funktion för `-bot`-grenen
3. ❌ **Modifiera `bookclub`** (Bash-skriptet) att anropa `python3 -m src.cli.sync_cli`
4. ❌ **Modifiera `bookclub.pi`** på samma sätt
5. ❌ **Testa** att alla kommandon fortfarande fungerar

### Fas 5: Lägg till Förbättringar (Dag 9–10) – **EJ PÅBÖRJAD**
**Nu när strukturen är stabil** kan vi lägga till förbättringar:

1. ❌ **Konfigurationsvalidering** – i `src/utils/config.py`, lägg till `validate_config()`
2. ❌ **Automatiska backup** – utöka `src/data/storage.py` för att skapa tidsstämplade backup
3. ❌ **Hälsokontroller** – lägg till `src/cli/health.py` som verifierar filbehörigheter, API-åtkomst, etc.
4. ❌ **Förbättrad loggning** – använd `src/utils/logging.py` för konsekventa, roterande loggfiler

### Fas 6: Testning & Slutlig Validering (Dag 11) – **EJ PÅBÖRJAD**
**Mål**: Säkerställ att allt fungerar på både PC och Raspberry Pi.

1. ❌ **Skriv några nyckelenhetstester** (med `pytest`)
2. ❌ **Testa på Raspberry Pi** (eller simulera med Docker)
3. ❌ **Verifiera bakåtkompatibilitet** – alla befintliga kommandon, miljövariabler och filformat måste förbli oförändrade
4. ❌ **Dokumentera den nya strukturen** i `README.md`

## 🗂️ Mål-filstruktur (Efter Migrering)

```
bookclub/
├── bookclub.pi                      # Pi launcher
├── bookclub                         # PC launcher
├── src/                             # Modulärt Python-paket
│   ├── cli/                         # CLI entry points
│   ├── sync/                        # Goodreads sync-logik
│   ├── bot/                         # Telegram bot
│   ├── data/                        # Data layer (file I/O, modeller)
│   └── utils/                       # Cross-cutting utilities
├── scripts/                         # Fristående exekverbara skript
├── config/                          # Applikationskonstanter
├── data/                            # Genererat innehåll (git-ignorerad)
├── logs/                            # Loggfiler (git-ignorerad)
└── tests/                           # Testfiler
```

## ⚙️ Tekniska Krav & Kompatibilitet
### Raspberry Pi (Volumio)
- Python 3.7+
- curl för Goodreads API
- Öppen port för webhook (om extern bot)
- Tillräckligt diskutrymme för bokloggar

### Bot-plattform
- Internetuppkoppling
- Bot-token/API-nyckel
- Webhook-support (för Telegram/Discord)

## 🧪 Teststrategi – Vad som ska valideras i varje fas

| Fas | Vad som ska testas | Kommando |
|-----|-------------------|----------|
| 0 | `bookclub.pi` exekverar | `./bookclub.pi -h` |
| 1 | Ny sync producerar identisk utdata | `diff reading_log.md reading_log.md.backup` |
| 2 | Data-lagret läser/skriver korrekt | `python -c "from src.data import storage"` |
| 3 | Refaktorerad bot startar och svarar | `python scripts/telegram_bot_refactored.py` |
| 4 | Launcher-skripten fungerar fortfarande | `./bookclub -sync && ./bookclub.pi -sync` |
| 5 | Förbättringar bryter inget | Kör alla befintliga kommandon |
| 6 | Allt fungerar på Pi | (faktiskt Pi-test) |

## 🚨 Risker & Åtgärder

| Risk | Åtgärd |
|------|--------|
| Bryta den fungerande synken | Behåll original `sync_books.py` tills den nya modulen passerar diff-testet |
| Bryta Telegram-boten | Kör den refaktorerade boten parallellt med test-token innan byte |
| Raspberry Pi-kompatibilitet | Testa `bookclub.pi` efter varje fas; håll dess beroenden minimala |
| Dataförlust | Skapa alltid backup innan något kärnskript ersätts |

## 🚀 Nästa Steg

**Aktuell fokus: Fas 3 (Refaktorera Telegram-boten).**  
Fas 2 är helt klar. Nu fortsätter vi med Fas 3:  

1. **Skapa `src/bot/core.py`** – flytta `main()`, applikationsbyggare, felhanterare.
2. **Skapa `src/bot/middleware/auth.py`** – flytta `@auth_only`-dekoratorn.
3. **Skapa `src/bot/middleware/formatters.py`** – flytta formateringsfunktioner.

Kör följande kommandon för att kolla status:

```bash
# Kontrollera att src/sync modulerna redan finns
ls -la src/sync/
# Kontrollera att data-katalogen finns men saknar implementering
ls -la src/data/
# Testa att den refaktorerade sync-scriptet fungerar
python3 scripts/sync_books_refactored.py
```

## 🔗 Resurser
- [python-telegram-bot dokumentation](https://github.com/python-telegram-bot/python-telegram-bot)
- [Goodreads API dokumentation](https://www.goodreads.com/api)
- [Raspberry Pi cron guide](https://www.raspberrypi.com/documentation/computers/os.html#cron)

## 📞 Support Under Migrering
- Om något går fel, återgå till backup-kopior (`*.backup`)
- Testa efter **varje filändring**
- Använd `git diff` för att se exakt vad som modifieras
- Håll denna `ROADMAP.md` öppen och markera avslutade steg

---
*Senast uppdaterad: 2026-02-13*
*Status: Fas 1 & 2 slutförda, Fas 3 påbörjad – Nästa steg är att refaktorera botens kärna.*
