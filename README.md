# Bokklubb-synkronisering

Ett litet Bash/Python-verktyg för att synkronisera lästa böcker från Goodreads till en lokal Markdown-logg.

## Funktioner
- Hämtar dina lästa böcker från Goodreads via RSS
- Genererar en snygg Markdown-tabell med metadata (titel, författare, betyg, datum, länk)
- Stöd för diskussion om böcker via AI-assistent (Grok/DeepSeek)
- Automatisk städning av temporära filer
- **Telegram-bot** för att visa läslogg och pågående läsning via chatt

## Krav
- Python 3.10+
- Zsh eller Bash
- Goodreads API-nyckel (gratis)

## Snabbsättup
1. Klona repot
2. Skapa `.env`-fil med din Goodreads API-nyckel och användar-ID:
   ```
   GOODREADS_API_KEY='din_nyckel_här'
   GOODREADS_USER_ID='ditt_user_id_här'
   ```
   Hitta ditt User ID på [goodreads.com/settings](https://www.goodreads.com/settings)
3. Kör `./bookclub -sync` för att hämta och generera loggen

## Användning
```bash
# Synkronisera böcker från Goodreads
./bookclub -sync

# Starta AI-chatt om dina böcker (använder Grok)
./bookclub -chat

# Utvecklingsläge med DeepSeek
./bookclub -dev

# Starta Telegram-boten
./bookclub.pi -bot
```

## Telegram Bot Setup
1. Installera bot‑beroenden:
   ```bash
   pip install -r requirements.txt
   ```
2. Skapa en bot via [@BotFather](https://t.me/botfather) på Telegram och kopiera token.
3. Lägg till token i `.env`:
   ```
   TELEGRAM_BOT_TOKEN='din_bot_token_här'
   ```
4. Kör `python3 get_chat_id.py` för att få ditt användar‑ID (skicka ett meddelande till din bot först).
5. Lägg till ID:t i `.env`:
   ```
   TELEGRAM_CHAT_ID='ditt_chat_id_här'
   ```
6. Starta boten:
   ```bash
   ./bookclub.pi -bot
   ```

## System Health
To verify that the environment is correctly configured (especially on Raspberry Pi):
```bash
python3 -m src.cli.health
```

## Automatisk Synkronisering (Cron)
För att automatiskt synkronisera dina böcker varje dag, lägg till följande cron-jobb:

```bash
# Öppna crontab för redigering
crontab -e
```

Lägg till följande rad för att köra synkronisering varje dag kl 02:00:
```
0 2 * * * cd /sökväg/till/bookclub && ./bookclub.pi -sync >> /var/log/bookclub_sync.log 2>&1
```

Eller för att testa varje timme:
```
0 * * * * cd /sökväg/till/bookclub && ./bookclub.pi -sync >> /var/log/bookclub_sync.log 2>&1
```

Se till att skriptet är körbart:
```bash
chmod +x bookclub.pi
```

### Bot‑kommandon
- `/start` – Välkomstmeddelande
- `/help` – Visa tillgängliga kommandon
- `/books` – Visa hela läsloggen
- `/progress` – Visa pågående läsning
- `/discuss` – Starta en diskussion om böckerna

## Filer
- `bookclub` – Huvudskript (Bash)
- `sync_books.py` – Bearbetar XML och genererar Markdown
- `reading_log.md` – Genererad läslogg (skapas vid första sync)
- `reading_in_progress.md` – Pågående läsning (skapas manuellt)
- `BOKKLUBB.md` – Instruktioner för AI-assistent
- `telegram_bot.py` – Telegram‑bot (modern version)
- `get_chat_id.py` – Hjälpscript för att hämta ditt chat‑ID
- `requirements.txt` – Beroenden för bot‑funktionalitet

## Arbetsflöde
1. `-sync` hämtar RSS-data för ditt användar-ID → skapar `raw_books.xml` → bearbetar till `reading_log.md`
2. `-chat` läser `reading_log.md` och startar AI-chatt om böcker
3. Temporära filer raderas automatiskt efter synk
4. Personliga bokfiler (`reading_log.md`, `reading_in_progress.md`) är ignorerade i git
5. Boten kan användas oberoende för att fråga om läsloggen via Telegram

## Licens
MIT
