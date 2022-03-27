Configurar mosquito:

    En Windows Mosquitto se inicia como un servicio. Agregar las siguientes líneas a mosquitto.config donde se instaló el programa:

    listener 1883 127.0.0.1
    allow_anonymous true
    persistence true
    persistence_location C:/ProgramData/mosquitto
    autosave_interval 1
    autosave_on_changes true
    max_queued_messages 10000

    En Linux agregar un archivo .config en /etc/mosquitto/conf.d con las siguientes líneas:

    listener 1883 127.0.0.1
    allow_anonymous true
    autosave_interval 1
    autosave_on_changes true
    max_queued_messages 10000

    Las siguientes líneas son para que funcione con HiveMQ:

    connection hivemq
    address b94fa7cf0c0f4fcd91c97460db5c0564.s2.eu.hivemq.cloud:8883

    topic # both 2
    bridge_cafile /home/pi/Repositories/raspberry_pi_collector/certificates/isrgrootx1.pem
    remote_username AgriIntel
    remote_password Qwerty135
    bridge_protocol_version mqttv311
    try_private false
    notifications false
    bridge_attempt_unsubscribe false
    bridge_insecure true

Instalar paho-mqtt:

    pip install paho-mqtt

Para que funcione en la Raspberry Pi es posible que haya que instalar los drivers de XDS110:

https://software-dl.ti.com/ccs/esd/documents/xdsdebugprobes/emu_xds_software_package_download.html
