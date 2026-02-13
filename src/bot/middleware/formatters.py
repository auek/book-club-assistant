import logging

logger = logging.getLogger(__name__)

def format_books_for_telegram(markdown_text: str) -> str:
    """Convert markdown table to a more readable Telegram format."""
    lines = markdown_text.split('\n')
    formatted_lines = []
    in_table = False
    book_count = 0
    table_rows = []
    
    for line in lines:
        if line.startswith('|') and 'Titel' in line and 'Författare' in line:
            in_table = True
            continue
        elif line.startswith('|') and in_table:
            table_rows.append(line)
        elif line.startswith('## Sammanfattning'):
            in_table = False
    
    for i, line in enumerate(table_rows):
        parts = [part.strip() for part in line.split('|') if part.strip()]
        if len(parts) >= 5:
            title, author, rating, date, link = parts[0], parts[1], parts[2], parts[3], parts[4]
            book_count += 1
            try:
                rating_int = int(rating)
                stars = '⭐' * rating_int + '☆' * (5 - rating_int) if rating_int <= 5 else rating
            except ValueError:
                stars = rating
            
            formatted_lines.append(f"<b>{book_count}. {title}</b>")
            formatted_lines.append(f"   👤 <i>{author}</i>")
            formatted_lines.append(f"   {stars} | 📅 {date}")
            if i < len(table_rows) - 1:
                formatted_lines.append("")
    
    in_summary = False
    for line in lines:
        if line.startswith('## Sammanfattning'):
            formatted_lines.append("\n📊 <b>Sammanfattning</b>")
            in_summary = True
        elif in_summary and line.startswith('- **'):
            if 'Totalt antal böcker:' in line:
                formatted_lines.append(line.replace('- **', '📚 ').replace('**', ''))
            elif 'Högsta betyg:' in line:
                formatted_lines.append(line.replace('- **', '🏆 ').replace('**', ''))
            elif 'Senaste bok:' in line:
                formatted_lines.append(line.replace('- **', '🆕 ').replace('**', ''))
            elif 'Äldsta bok:' in line:
                formatted_lines.append(line.replace('- **', '📜 ').replace('**', ''))
    
    if book_count == 0:
        return f"📚 <b>Lästa Böcker</b>\n\n{markdown_text}"
    
    return f"📚 <b>Lästa Böcker</b> ({book_count} böcker)\n\n" + "\n".join(formatted_lines)

def format_progress_for_telegram(markdown_text: str) -> str:
    """Format the reading progress markdown for nice Telegram display."""
    if not markdown_text.strip():
        return "📖 <b>Pågående läsning</b>\n\nInga böcker i pågående läsning för tillfället."
    
    lines = markdown_text.strip().split('\n')
    formatted_lines = ["📖 <b>Pågående läsning</b>\n"]
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith('# '): formatted_lines.append(f"\n<b>{line[2:]}</b>")
        elif line.startswith('## '): formatted_lines.append(f"\n<i>{line[3:]}</i>")
        elif line.startswith('- '): formatted_lines.append(f"• {line[2:]}")
        elif '[' in line and ']' in line and '(' in line and ')' in line:
            try:
                text_start, text_end = line.find('['), line.find(']')
                url_start, url_end = line.find('('), line.find(')')
                if text_start < text_end < url_start < url_end:
                    text, url = line[text_start+1:text_end], line[url_start+1:url_end]
                    formatted_lines.append(line[:text_start] + f'<a href="{url}">{text}</a>' + line[url_end+1:])
                else: formatted_lines.append(line)
            except: formatted_lines.append(line)
        else: formatted_lines.append(line)
    
    formatted_lines.append("\n\n📌 <i>Uppdatera filen reading_in_progress.md för att ändra</i>")
    return '\n'.join(formatted_lines)

def split_text_into_chunks(text: str, max_length: int = 4096) -> list:
    """Split text into chunks that don't exceed max_length."""
    if len(text) <= max_length: return [text]
    chunks, current_chunk = [], ""
    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + "\n"
        else:
            if current_chunk: chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
    if current_chunk: chunks.append(current_chunk.strip())
    return chunks
