import os
import httpx
from openai import AsyncOpenAI
from src.data.storage import read_file_content

async def get_ai_response(user_query: str, history: list = None) -> str:
    """Get a response from the LLM based on the reading log context."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    model = os.getenv('CHAT_MODEL', 'google/gemini-2.0-flash-001')
    
    if not api_key:
        return "❌ AI-tjänsten är inte konfigurerad (saknar OPENROUTER_API_KEY)."

    # Load context
    reading_log = read_file_content("reading_log.md")
    reading_in_progress = read_file_content("reading_in_progress.md")
    instructions = read_file_content("BOKKLUBB.md")
    
    # Use a custom httpx client to avoid proxy-related initialization errors
    http_client = httpx.AsyncClient(proxies={})
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        http_client=http_client,
    )

    system_prompt = f"""
    {instructions}
    
    Här är användarens nuvarande läslogg:
    {reading_log}

    Här är vad användaren läser just nu:
    {reading_in_progress}
    
    Svara på svenska. Var kortfattad men engagerande.
    """

    # Guardrail: Limit input length to save tokens
    if len(user_query) > 1000:
        return "❌ Frågan är för lång (max 1000 tecken)."

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_query})

    try:
        # Guardrail: Limit input length to save tokens
        if len(user_query) > 1000:
            return "❌ Frågan är för lång (max 1000 tecken)."

        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500  # Guardrail: Limit response length
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Ett fel uppstod vid kontakt med AI: {str(e)}"
