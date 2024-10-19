import os
from openai import OpenAI
import json

# Set up the OpenAI client
client = OpenAI(
)

def translate_text(language: str, text: str) -> str:
    """
    This function translates a given text into a specified language using OpenAI's API.
    """
    messages = [
        {
            "role": "system",
            "content": f"You are a professional translator. Translate the following English text into {language}."
        },
        {
            "role": "user",
            "content": text
        }
    ]

    # Make a request to OpenAI to translate the text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500
    )

    # Extract the translation from the response
    translated_text = response.choices[0].message.content.strip()
    return translated_text

def main():
    print("Welcome to the CLI Language Translator!\n")

    # Input the target language and text to translate
    language = input("Enter the target language (e.g., Swahili, Zulu, etc.): ")
    text = input("Enter the English text to translate: ")

    # Perform the translation
    try:
        translated_text = translate_text(language, text)
        print(f"\nTranslation in {language}:")
        print(translated_text)
    except Exception as e:
        print("Error during translation:", str(e))

if __name__ == "__main__":
    main()
