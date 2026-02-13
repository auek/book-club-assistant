import os
from openai import AsyncOpenAI
from src.data.storage import read_file_content

async def get_ai_response(user_query: str) -> str:
    """Get a response from the LLM based on the reading log context."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    model = os.getenv('CHAT_MODEL', 'google/gemini-2.0-flash-001')
    
    if not api_key:
        return "❌ AI-tjänsten är inte konfigurerad (saknar OPENROUTER_API_KEY)."

    # Load context
    reading_log = read_file_content("reading_log.md")
    instructions = read_file_content("BOKKLUBB.md")
    
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    system_prompt = f"""
    {instructions}
    
    Här är användarens nuvarande läslogg:
    {reading_log}
    
    Svara på svenska. Var kortfattad men engagerande.
    """

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Ett fel uppstod vid kontakt med AI: {str(e)}"
