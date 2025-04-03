import os
import time
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import docker
import socket
import random

# Puertos >>>>>>
def find_available_port(start_port=1000, end_port=65535):
    port = random.randint(start_port, end_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    while True:
        try:
            sock.bind(('', port))
            sock.close() 
            return port
        except OSError:
            port = random.randint(start_port, end_port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Contenedores >>>>
dockerClient = docker.from_env()
# REDIS
def create_redis_cont(available_port):
    container = dockerClient.containers.run(
     "redis",
     name=f"redis-container-{available_port}",     
     ports={f'6379/tcp': available_port},          
     detach=True,                       
 )

    container.reload()

    client.chat_postMessage(channel=ai_id, text=f"Contenedor creado: \n Nombre: {container.name} \nID: {container.id} \nPuerto expuesto: {available_port}")

# Principal >>>>>> 
dotenv_path = Path(__file__).resolve().parent.parent / ".conf"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"Error: El archivo {dotenv_path} no se encuentra.")
    exit(1)

slack_key = os.getenv("SLACK_KEY")
client = WebClient(slack_key)
ai_id = os.getenv("CONTAINERS_SLACK_CHANNEL_ID")
supported_containers = os.getenv("CONTAINERS_SUPPORTED").split(",")

try:
    response = client.conversations_history(channel=ai_id, limit=1)
    last_timestamp = response['messages'][0]['ts'] if response.get('messages') else None
except SlackApiError as e:
    print(f"Error al obtener historial: {e.response['error']}")
    exit(1)


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

                    if message_text.startswith("Crear"):
                        container_value = message_text[5:].strip()

                        if container_value in supported_containers:
                            match container_value:
                                case "redis":
                                    available_port = find_available_port()
                                    create_redis_cont(available_port)
                                    
                        else:
                            client.chat_postMessage(channel=ai_id, text="No está soportado")

                    if message_text == "Listado":
                        client.chat_postMessage(channel=ai_id, text=f"Los contenedores soportados al momento son: {supported_containers}")

    except SlackApiError as e:
        print(f"Error: {e.response['error']}")
        if e.response['error'] == "ratelimited":
            retry_after = int(e.response.headers.get("Retry-After", 10))
            print(f"Rate limit alcanzado. Esperando {retry_after} segundos...")
            time.sleep(retry_after)

    time.sleep(5)
