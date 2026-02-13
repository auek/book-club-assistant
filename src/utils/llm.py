import os
import openai
from src.data.storage import read_file_content

def get_ai_response(user_query: str) -> str:
    """Get a response from the LLM based on the reading log context."""
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('DEEPSEEK_API_KEY')
    model = os.getenv('CHAT_MODEL', 'gpt-3.5-turbo')
    
    if not api_key:
        return "❌ AI-tjänsten är inte konfigurerad (saknar API-nyckel)."

    # Load context
    reading_log = read_file_content("reading_log.md")
    instructions = read_file_content("BOKKLUBB.md")
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url=os.getenv('LLM_BASE_URL') # Optional: for DeepSeek or local LLMs
    )

    system_prompt = f"""
    {instructions}
    
    Här är användarens nuvarande läslogg:
    {reading_log}
    
    Svara på svenska. Var kortfattad men engagerande.
    """

    try:
        response = client.chat.completions.create(
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
