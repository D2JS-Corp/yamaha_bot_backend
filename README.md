# ¿Cómo correr el proyecto?
## Requisitos
- Un Broker MQTT
## Paso a Paso
1. Necesitas crear el archivo .env en la raíz del proyecto. Estas son las variables que debe llevar dicho archivo
~~~ conf
PROJECT_NAME="Museum Robot API"
MQTT_BROKER_HOST="localhost"
MQTT_BROKER_PORT=1883
MQTT_CLIENT_ID="museum-admin-api"
MQTT_TOPICS='["ros2/chatter"]'
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_QOS=1
~~~
2. Accede desde tu consola a la raíz del proyecto, crea un entorno virtual e instala las dependencias
~~~ bash
# Usa el gestor de entornos de tu preferencia
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
~~~
3. Para correr el proyecto debes ubicarte en la carpeta padre del repositorio y desde allí podrás inicializarlo
~~~ bash
# Para ir a la carpeta superior
cd ..

uvicorn yamaha_bot_backend.main:app --reload
~~~