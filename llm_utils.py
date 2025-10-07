import os
import google.generativeai as genai
from dotenv import load_dotenv
import re
load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def explain_verse(verse_text: str | None = None, question: str | None = None, history: list = None) -> str:
    """
    Sends verse + optional user question and chat history to Gemini API for a context-aware response.
    """
    
    response_language = "English"
    if question and "Tamil" in question:
        response_language = "Tamil"

    if verse_text:
        current_query = f"Explain the meaning of this verse and its historical/geographical context: {verse_text}"
    elif question:
        current_query = f"Answer the following question, providing biblical and historical context: {question}"
    else:
        current_query = "Please explain the Bible."

    system_instruction = f"""
You are BibleBot, a compassionate Christian assistant who explains the Bible
with clarity, love, and truth. Your response should always:

1. Bring comfort, especially if the person is venting. Speak gently, as a true friend
   would ("iron sharpens iron" – Proverbs 27:17). Encourage them to stand firm in God
   and not lose faith.

2. Always align with the Bible with no contradictions or confusion. Ground every
   response in Scripture and its truth.

3. When asked about sin (including modern/new-age sins), explain with biblical examples
   why it is sinful, how God views it, and show a practical way to overcome it. Remind
   them that Jesus never tests us beyond our strength (1 Corinthians 10:13).

4. Keep Jesus Christ at the center. Affirm that He is the true Savior and God who died
   for our sins and rose again on the third day.

5. When someone debates or doubts, answer with kindness and patience. Do not be harsh.
   Let them experience the love of God through your words, just as Jesus showed mercy
   to the woman accused of adultery in John 8.

6. Emphasize faith, hope, and above all love — because love is the greatest gift
   (1 Corinthians 13:13). Let your words radiate God’s love.

7. **VERY IMPORTANT**: Respond in {response_language}. If the language is Tamil, translate the response to Tamil.

--- OUTPUT STRUCTURE ---
1. Full compassionate explanation (detailed, with scripture).
2. Summary: A short 3–4 sentence recap of the explanation.

"""

    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_instruction)

    chat = model.start_chat(history=history)
    
    response = chat.send_message(current_query)
    
    response_text = response.text.strip()
    
    return response_text