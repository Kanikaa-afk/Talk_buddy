import openai
from openai import OpenAI
import random

# Setup OpenRouter client using your API key and base URL
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# Jokes and quotes
jokes = [
    "Why did the computer go to the doctor? Because it had a virus!",
    "Teacher: Tum itni der se class mein kyun nahi aa rahe? Student: Sir, traffic tha, WhatsApp pe message bheja tha.",
    "What do you call a fish wearing a crown? A kingfish!",
    "Meri mom kehti hain, 'Beta, itna computer khelna chhodo.' Maine kaha, 'Mom, main programming kar raha hoon!'",
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Ek ladka apni girlfriend ko bola: Tum meri WiFi ho, bina tumhare main connect nahi ho paata."
]

quotes = [
    "Believe you can and you're halfway there.",
    "Zindagi mein kabhi himmat mat haarna, kyunki haar ke bhi jeet sakte ho.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Aaj kaam karo, kal ka tension kam karo.",
    "The best way to predict the future is to create it.",
    "Chhoti chhoti baaton mein khushi dhoondo, life set ho jayegi."
]

help_text = """
You can just chat naturally with me! Try saying:
- 'I want a joke' or 'Share a quote'
- 'I'm feeling sad' or 'I'm anxious today'
- 'Can you help me?' or even just 'hello'
"""

mood_history = []

def talk_to_buddy(user_input, mood=None):
    user_input_lower = user_input.lower()

    # Natural command triggers
    if "help" in user_input_lower:
        return help_text
    elif "mood" in user_input_lower:
        return "Recent moods: " + ", ".join(mood_history[-5:]) if mood_history else "No mood tracked yet."
    elif "joke" in user_input_lower:
        return random.choice(jokes)
    elif "quote" in user_input_lower or "motivation" in user_input_lower:
        return random.choice(quotes)
    elif any(word in user_input_lower for word in ["exit", "quit", "bye"]):
        return None

    # Mood input
    if user_input_lower in ["happy", "sad", "anxious", "angry", "neutral"]:
        mood_history.append(user_input_lower)
        return f"Mood updated to '{user_input_lower}'. How can I help you today?"

    # ChatGPT response via OpenRouter
    try:
        messages = [
            {"role": "system", "content": "You are a kind and caring emotional support chatbot. Reply with empathy."},
            {"role": "user", "content": user_input}
        ]

        if mood:
            messages.insert(1, {"role": "system", "content": f"The user feels {mood}. Respond accordingly."})

        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=messages,
            timeout=15
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Sorry, something went wrong. ❌\nError: {str(e)}"

# App start
if __name__ == "__main__":
    print("Talk Buddy is ready! (Type 'exit' or 'quit' to stop)")
    mood = input("How are you feeling today? (happy, sad, anxious, angry, neutral)\nYour mood: ").strip().lower()
    if mood in ["happy", "sad", "anxious", "angry", "neutral"]:
        mood_history.append(mood)

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Talk Buddy: Take care! 💛")
            break

        response = talk_to_buddy(user_input, mood)
        if response is None:
            print("Talk Buddy: Take care! 💛")
            break
        print("Talk Buddy:", response)
