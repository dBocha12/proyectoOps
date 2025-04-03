import os
import time
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

dotenv_path = Path(__file__).resolve().parent.parent / ".conf"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)

slack_key = os.getenv("SLACK_KEY")
client = WebClient(slack_key)
channel_id = os.getenv("AWS_SLACK_CHANNEL_ID")

last_timestamp = None


while True:
    try:
        response = client.conversations_history(channel=channel_id, limit=1)

        if 'messages' in response and response['messages']:
            latest_message = response['messages'][0]
            message_text = latest_message.get('text', '').strip().lower()
            message_timestamp = latest_message.get('ts', '')

            if message_timestamp != last_timestamp and message_text in ['tf', 'tf destroy']:
                last_timestamp = message_timestamp

                terraform_directory = Path(__file__).resolve().parent.parent / "functions" / "terraform"

                if not terraform_directory.exists():
                    client.chat_postMessage(channel=channel_id, text="Directorio de Terraform no encontrado.")
                    continue

                os.chdir(terraform_directory)

                if message_text == 'tf':
                    client.chat_postMessage(channel=channel_id, text="Iniciando creación de maquinaria en AWS con Terraform")
                    subprocess.run(["terraform", "init"], check=True)
                    subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
                    client.chat_postMessage(channel=channel_id, text="AWS creada con éxito!")

                elif message_text == 'tf destroy':
                    client.chat_postMessage(channel=channel_id, text="Destruyendo infra en AWS con Terraform")
                    subprocess.run(["terraform", "init"], check=True)
                    subprocess.run(["terraform", "destroy", "-auto-approve"], check=True)
                    client.chat_postMessage(channel=channel_id, text="Infraestructura destruida!")

    except SlackApiError as e:
        print(f"Error con Slack API: {e.response['error']}")
        if e.response['error'] == "ratelimited":
            retry_after = int(e.response.headers.get("Retry-After", 10))
            print(f"Rate limit alcanzado. Esperando {retry_after} segundos...")
            time.sleep(retry_after)

    time.sleep(5)
