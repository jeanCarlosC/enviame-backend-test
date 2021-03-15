# enviame-backend-test
# Introducción
Primero que todo, darle muchas gracias a enviame por darme la oportunidad de iniciar este proceso y espero cumplir sus espectativas para el cargo.

Todos los ejercicios fueron desarrollados bajo el lenguaje de PYTHON junto con el framework FLASK y ORM SQLAlchemy para menejo de consultas SQL.

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
* Instalar Docker
* Instalar Docker compose


# Ejercicio 1
1. Desde la consola posicionarte en la raiz del proyecto
2. Ejecutar el docker compose con la siguiente linea de comando docker-compose up --build, esperar que se instalen las dependencias y que se inicializen ambos contenedores. en caso de querer iniciar como demonio y no deje tomada la consola, agregar el parametro -d en la linea de comando : docker-compose up -d --build

En el archivo docker-compose se encuentra toda la condiguración para el levantamiento de los contenedores "enviame" para la aplicación y dbmysql para la base de datos mysql

# Ejercicio 2

Al ejecutar los contenedores docker tendremos disponible en los servicios para el CRUD del ejercicio 2

URL development : http://localhost:5000/

# Servicio para listar todas las compañias
http://localhost:5000/companies
Method : GET

# Servicio para obtener una compañia en base al id
http://localhost:5000/company/1
Method : GET

# Servicio para crear una compañia

http://localhost:5000/company/create
Method: POST
Headers: {
    "Content-Type":"application/json"
}
body : {
	"identification":"1231234",
	"name":"Emviame SPA",
	"address": "Manquehue 105, las condes, santiago de chile",
	"mail":"contact@enviame.io"
}

# Servicio para editar una compañia

http://localhost:5000/company/create
Headers: {
    "Content-Type":"application/json"
}
body : {
	"identification":"1231234",
	"name":"Emviame SPA",
	"address": "Manquehue 105, las condes, santiago de chile",
	"mail":"contact@enviame.io"
}
Los datos son opcionales excepto la identificacion

# Servicio para eliminar una compañia

http://localhost:5000/company/delete/1

La estructura de la respuesta para todos los servicios es la siguiente

{
    "success": True,
    "message": "Successfully created company",
    "data":{}
}

En caso de error el atributo data no viene en la respuesta.

# Ejercicio 3

http://localhost:5000/palindrome
Method : GET

Servicio con el cual llamo el script para evaluar los substring palindromos dentro de la cadena texto dada, en caso de querer probar otra cadena puedes enviar el parametro "string" con el texto

# Ejercicio 4

http://localhost:5000/scripts/createDelivery
Method : POST

servicio el cual consume servicio de enviame y guarda la respuesta en una tabla log dentro del contenedor mysql

# Ejercicio 5
http://localhost:5000/scripts/DeliveryTime
Method : GET

Servicio con el cual llamo el script para conocer el numeros de dias de entrega de una compra online, basado en la secuencia fibonacci
cada vez que se hace el consumo, se llama el escript con un numero aleatorio de 0 a 2000, en caso de que se quisiera evaluar una distancia especifica, podrías enviar el parametro "km" con el numero de kilometros a evaluar.

# Ejercicio 6
Flatante

# Ejercicio 7

Para este ejercicio contruí la siguiente query:

SET SQL_SAFE_UPDATES = 0;
update employees 
join countries on countries.id = employees.country_id
join continents on continents.id = countries.continent_id
SET employees.salary = employees.salary + round((continents.anual_adjustment/100) * employees.salary,0)
WHERE employees.salary <= 5000;
SET SQL_SAFE_UPDATES = 0;

Donde se inabilita el safe_update para ejecutar el update y luego se habilita nuevamente.
