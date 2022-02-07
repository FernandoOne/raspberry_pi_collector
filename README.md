Configurar mosquito:

En Windows Mosquitto se inicia como un servicio. Agregar las siguientes líneas a mosquitto.config donde se instaló el programa:

listener 1883 127.0.0.1
allow_anonymous true
persistence true
persistence_location C:/ProgramData/mosquitto
autosave_interval 1
autosave_on_changes true
max_queued_messages 10000
