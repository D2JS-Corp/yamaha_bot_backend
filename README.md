# 🤖 Museum Robot API

Este proyecto implementa un **backend en FastAPI** para el panel administrativo de un **robot guía turístico de museo**.  
La API consume datos del robot a través del protocolo **MQTT** y los expone en una **API REST** para que puedan ser consumidos por un frontend.

---

## Estructura del proyecto

```

app/
│── api/                # Endpoints REST
│── core/               # Configuración y settings
│── domain/             # Modelos de dominio
│── infrastructure/     # Integraciones externas
│── services/           # Lógica de negocio
│── main.py             # Punto de entrada FastAPI

````

---

## Requisitos

- Python **3.10+**
- [pip](https://pip.pypa.io/)
- Un broker **MQTT** (ej: Mosquitto)

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/D2JS-Corp/YamahaBotBackend.git
cd YamahaBotBackend
````

2. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux / MacOS
venv\Scripts\activate      # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
   Crea un archivo `.env` en la raíz del proyecto:

```env
PROJECT_NAME="Museum Robot API"
MQTT_BROKER_HOST=
MQTT_BROKER_PORT=
MQTT_TOPIC=
DATABASE_URL=
```

---

## Ejecución

Iniciar la API:

```bash
uvicorn main:app --reload
```

La API estará disponible en:

* Documentación Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* Documentación ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---


## Autor

Desarrollado por ***D2JS*** 🪙

---