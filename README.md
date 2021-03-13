# enviame-backend-test
# Introducción
Primero que todo, darle muchas gracias a enviame por darme la oportunidad de iniciar este proceso y espero cumplir sus espectativas para el cargo.

Todos los ejercicios fueron desarrollados bajo el lenguaje de PYTHON junto con el framework FLASK

Para el ambiente de desarrollo se utilizaron 2 contenedores, 1 para levantar la aplicación con python flask y otro para el manejo de la base de datos mysql

Se manejaron 2 volumenes para la persistencia de datos para la aplicación (datos_enviame) y nuestra base de datos (dbmysql).

Con la siguiente url http://localhost:5000 o http://127.0.0.1:5000 se tendrá acceso a los servicios y scripts 

Los datos de acceso de la base de datos (configurables en el archivo docker-compose) son los siguientes:
* Hostname : 127.0.0.1
* Port : 8084
* Username : enviame
* Password : enviame12345
* Root password : root12345
* Base de datos : db



# Requerimientos para levantar el ambiente de desarrollo
* Docker
* Docker compose

# Pasos a seguir para levantar ambiente de desarrollo
1. Desde la consola posicionarte en la raiz del proyecto
2. Ejecutar el docker compose con la siguiente linea de comando docker-compose up --build, esperar que se instalen las dependencias y que se inicializen ambos contenedores. en caso de querer iniciar como demonio y no deje tomada la consola, agregar el parametro -d en la linea de comando : docker-compose up -d --build