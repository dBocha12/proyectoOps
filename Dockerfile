FROM python:3.11-slim

WORKDIR /app

COPY src/ /app/
COPY src/.conf /app/.conf

RUN apt-get update && \
    apt-get install -y wget unzip ca-certificates curl gnupg lsb-release && \
    wget https://releases.hashicorp.com/terraform/1.4.6/terraform_1.4.6_linux_amd64.zip && \
    unzip terraform_1.4.6_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_1.4.6_linux_amd64.zip

RUN pip install --no-cache-dir slack_sdk python-dotenv openai docker

ENV CHATOPS_CONF_PATH=/app/.conf

CMD ["python", "main.py"]
