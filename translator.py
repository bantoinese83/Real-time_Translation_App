# translator.py
from openai import OpenAI


class Translator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history = []

    def clear_conversation_history(self):
        self.conversation_history.clear()

    def translate_text(self, user_text: str, source_language: str, target_language: str, max_tokens: int = 300) -> str:
        prompt = (
            f"Translate the following text from {source_language} to {target_language}:\n"
            f"{user_text}"
        )

        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.conversation_history,
            max_tokens=max_tokens,
        )

        translated_text = response.choices[0].message.content.strip()

        self.conversation_history.append({
            "role": "assistant",
            "content": translated_text
        })

        return translated_text
