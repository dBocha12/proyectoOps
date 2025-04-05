# 🧪 Proyecto InvOps
## Integrantes
* Daniel Bolanos Chaves
* Ivnaia Miranda Chacon
* Jeremy Ruiz Camacho

ChatOps integrado con 3 funcionalidades, entre ellas:


### Terraform:
Modulo con dos comandos **tf** y **tf destroy** para poder crear y eliminar instacias usando Terraform en AWS.

### AI:
Modulo con un comando **AI:** donde lo que le siga a "AI: sera utilizado en un prompt enviado por medio de API a OpenAI"

### Contenedores:
Modulo con un comando **Crear** y por el momento con una sola opcion "redis", donde con un solo comando creara un contenedor de Redis DB, buscando un puerto disponible y usandolo para exponer la DB.

## 🛠️ Prerequisitos

- Docker
- Bot de [Slack](https://api.slack.com/apps)
- Crear una llave de seguridad (Key pair) en AWS llamada test-kp, si se desea usar el Terraform integrado


---

## 🚀 ¿Cómo ejecutar el proyecto?

Sigue estos pasos para configurar y ejecutar el código:

### 1. Clonar el repositorio

```bash
git clone https://github.com/dBocha12/proyectoOps.git
```

### 2. Configurar archivo `.conf`

Edita `config.conf` con los valores adecuados. Consulta la tabla de parámetros más abajo para ver las opciones válidas.

### 3. Ejecutar el programa

**Windows:**
```bash
.\ejecutar_windows.ps1
```

**MAC/Linux:**
```bash
.\ejecutar_linux_mac.sh
```

---

## ⚙️ Parámetros de Configuración (`.conf`)

### 🧱 Obligatorios

| Parámetro                   | Descripción                                               | Valores posibles                  | Por defecto |
|----------------------------|-----------------------------------------------------------|-----------------------------------|-------------|
| `SLACK_KEY`                | API Key del bot de Slack                                  | `xoxb-XXXXXXXXXXXXX`              | `N/A`       |
| `CHATOPS_SLACK_CHANNEL_ID` | Canal general donde el bot anunciará su funcionamiento     | ID de canal Slack (ej: `C08XXX`)  | `N/A`       |
| `CHATOPS_TERRAFORM`        | Activa el módulo de integración con Terraform              | `true`, `false`                   | `true`      |
| `CHATOPS_AI`               | Activa el módulo de inteligencia artificial                | `true`, `false`                   | `true`      |
| `CHATOPS_CONTAINERS`       | Activa el módulo de gestión de contenedores                | `true`, `false`                   | `true`      |

---

### ☁️ Terraform (si `CHATOPS_TERRAFORM=true`)

| Parámetro               | Descripción                                    | Valores posibles                      | Por defecto |
|------------------------|------------------------------------------------|---------------------------------------|-------------|
| `AWS_ACCESS_KEY_ID`    | Clave pública AWS                              | Cadena alfanumérica                   | `N/A`       |
| `AWS_SECRET_ACCESS_KEY`| Clave secreta AWS                              | Cadena secreta                        | `N/A`       |
| `AWS_DEFAULT_REGION`   | Región predeterminada AWS                      | `us-east-1`, `us-west-2`, etc.        | `us-east-1` |
| `AWS_SLACK_CHANNEL_ID` | Canal donde se anuncian eventos de Terraform   | ID de canal Slack                     | `N/A`       |

---

### 🤖 AI (si `CHATOPS_AI=true`)

| Parámetro            | Descripción                                | Valores posibles       | Por defecto |
|---------------------|--------------------------------------------|------------------------|-------------|
| `AI_API_KEY_ID`     | API Key de proveedor de AI (ej: OpenAI)    | `sk-...`               | `N/A`       |
| `AI_SLACK_CHANNEL_ID`| Canal donde se notifican respuestas de AI  | ID de canal Slack      | `N/A`       |

---

### 📦 Contenedores (si `CHATOPS_CONTAINERS=true`)

| Parámetro                     | Descripción                                         | Valores posibles                        | Por defecto |
|------------------------------|-----------------------------------------------------|-----------------------------------------|-------------|
| `CONTAINERS_SLACK_CHANNEL_ID`| Canal para notificaciones de contenedores           | ID de canal Slack                       | `N/A`       |
| `CONTAINERS_SUPPORTED`       | Lista separada por comas de contenedores soportados | `redis`, `grafana/grafana`, etc.        | `redis`     |


Ejemplo de archivo `config.conf`:

```
# OBLIGATORIO: Configuracion para funcionalidad basica del bot
SLACK_KEY=
CHATOPS_SLACK_CHANNEL_ID=
CHATOPS_TERRAFORM=true
CHATOPS_AI=true
CHATOPS_CONTAINERS=true


# OPCIONAL: Configuracion para Terraform <> AWS, CHATOPS_TERRAFORM debe ser "true"
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
AWS_SLACK_CHANNEL_ID=

# OPCIONAL: Configuracion para AI <> BOT, CHATOPS_AI debe ser "true"
AI_API_KEY_ID=
AI_SLACK_CHANNEL_ID=

# OPCIONAL: Configuracion para CONTENEDORES <> BOT, CHATOPS_CONTAINERS debe ser "true"
CONTAINERS_SLACK_CHANNEL_ID=
CONTAINERS_SUPPORTED=redis,grafana/grafana,prom/prometheus
```

---
