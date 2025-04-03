import os
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import threading

dotenv_path = Path(".conf")
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"Error: El archivo {dotenv_path} no se encuentra.")
    exit(1)

general_id = os.getenv("CHATOPS_SLACK_CHANNEL_ID")

aws_tf_enabled = os.getenv("CHATOPS_TERRAFORM", "").strip().lower()
ai_enabled = os.getenv("CHATOPS_AI", "").strip().lower()
containers_enabled = os.getenv("CHATOPS_CONTAINERS", "").strip().lower()

slack_key = os.getenv("SLACK_KEY")
client = WebClient(slack_key)

client.chat_postMessage(channel=general_id, text="Iniciando ChatOpsAI con la siguiente configuracion:")

def run_module(path):
    import subprocess
    subprocess.run(["python", path], check=True)

# TERRAFORM
if aws_tf_enabled == 'true':
    client.chat_postMessage(channel=general_id, text="TERRAFORM: El modulo esta habilitado")
    threading.Thread(target=run_module, args=("modules/terraform.py",)).start()
else:
    client.chat_postMessage(channel=general_id, text="TERRAFORM: El modulo esta deshabilitado")

# AI
if ai_enabled == 'true':
    client.chat_postMessage(channel=general_id, text="AI: El modulo esta habilitado")
    threading.Thread(target=run_module, args=("modules/ai.py",)).start()
else:
    client.chat_postMessage(channel=general_id, text="AI: El modulo esta deshabilitado")

# CONTENEDORES
if containers_enabled == 'true':
    client.chat_postMessage(channel=general_id, text="CONTENEDORES: El modulo esta habilitado")
    threading.Thread(target=run_module, args=("modules/docker_chat.py",)).start()
else:
    client.chat_postMessage(channel=general_id, text="CONTENEDORES: El modulo esta deshabilitado")
