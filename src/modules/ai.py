import os
import time
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from openai import OpenAI, APIError

dotenv_path = Path(".conf")
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"Error: El archivo {dotenv_path} no se encuentra.")
    exit(1)

slack_key = os.getenv("SLACK_KEY")
api_id_key = os.getenv("AI_API_KEY_ID")

client = WebClient(slack_key)
openai_client = OpenAI(api_key=api_id_key)

ai_id = os.getenv("AI_SLACK_CHANNEL_ID")

try:
    response = client.conversations_history(channel=ai_id, limit=1)
    last_timestamp = response['messages'][0]['ts'] if response.get('messages') else None
except SlackApiError as e:
    print(f"Error al obtener historial: {e.response['error']}")
    exit(1)

print(f"Último timestamp registrado: {last_timestamp}")

while True:
    try:
        response = client.conversations_history(channel=ai_id, oldest=last_timestamp, limit=10)

        if 'messages' in response and response['messages']:
            for message in reversed(response['messages']): 
                message_text = message.get('text', '').strip()
                message_timestamp = message.get('ts', '')

                if 'bot_id' in message:
                    continue  

                if last_timestamp is None or float(message_timestamp) > float(last_timestamp):
                    last_timestamp = message_timestamp 

                    if message_text.startswith("AI:"):
                        ai_content = message_text[3:].strip()
                        print(f"Mensaje de AI detectado: {ai_content}")

                        try:
                            completion = openai_client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[{"role": "user", "content": ai_content}]
                            )

                            ai_response = completion.choices[0].message.content
                            print(f"Respuesta de AI: {ai_response}")

                            client.chat_postMessage(channel=ai_id, text=ai_response)

                        except APIError as e:
                            print(f"Error con OpenAI: {e}")

    except SlackApiError as e:
        print(f"Error: {e.response['error']}")
        if e.response['error'] == "ratelimited":
            retry_after = int(e.response.headers.get("Retry-After", 10)) 
            print(f"Rate limit alcanzado. Esperando {retry_after} segundos...")
            time.sleep(retry_after)

    time.sleep(5)  
