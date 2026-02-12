# Bokklubb-synkronisering

Ett litet Bash/Python-verktyg för att synkronisera lästa böcker från Goodreads till en lokal Markdown-logg.

## Funktioner
- Hämtar dina lästa böcker från Goodreads via RSS
- Genererar en snygg Markdown-tabell med metadata (titel, författare, betyg, datum, länk)
- Stöd för diskussion om böcker via AI-assistent (Grok/DeepSeek)
- Automatisk städning av temporära filer

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
```

## Filer
- `bookclub` – Huvudskript (Bash)
- `sync_books.py` – Bearbetar XML och genererar Markdown
- `reading_log.md` – Genererad läslogg (skapas vid första sync)
- `reading_in_progress.md` – Pågående läsning (skapas manuellt)
- `BOKKLUBB.md` – Instruktioner för AI-assistent

## Arbetsflöde
1. `-sync` hämtar RSS-data för ditt användar-ID → skapar `raw_books.xml` → bearbetar till `reading_log.md`
2. `-chat` läser `reading_log.md` och startar AI-chatt om böcker
3. Temporära filer raderas automatiskt efter synk
4. Personliga bokfiler (`reading_log.md`, `reading_in_progress.md`) är ignorerade i git

## Licens
MIT
