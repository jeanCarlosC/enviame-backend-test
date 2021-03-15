# enviame-backend-test
# Introducción
Primero que todo, darle muchas gracias a enviame por darme la oportunidad de iniciar este proceso y espero cumplir sus espectativas para el cargo.

Todos los ejercicios fueron desarrollados bajo el lenguaje de PYTHON junto con el framework FLASK y ORM SQLAlchemy para menejo de consultas SQL.

Para el ambiente de desarrollo se utilizaron 2 contenedores, 1 para levantar la aplicación con python flask y otro para el manejo de la base de datos mysql

Se manejaron 2 volúmenes para la persistencia de datos para la aplicación (datos_enviame) y nuestra base de datos (dbmysql).

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
1. Desde la consola posicionarte en la raíz del proyecto
2. Ejecutar el docker compose con la siguiente línea de comando docker-compose up --build, esperar que se instalen las dependencias y que se inicializen ambos contenedores. en caso de querer iniciar como demonio y no deje tomada la consola, agregar el parámetro -d en la línea de comando : docker-compose up -d --build

y para consultar el estado de los contenedores podrás ejecutar el siguiente comando: "docker ps" y se listaran los contenedores que se encuentren activos

En el archivo docker-compose se encuentra toda la configuración para el levantamiento de los contenedores "enviame" para la aplicación y dbmysql para la base de datos mysql

# Ejercicio 2

Al ejecutar los contenedores docker tendremos disponible en los servicios para el CRUD del ejercicio 2

URL development : http://localhost:5000/

# Servicio para crear compañías faker
http://localhost:5000/scripts/fakeCompanies
Method : GET

se debe enviar el parámetro "quantity" que será la cantidad de compañías faker que creará 

# Servicio para listar todas las compañías
http://localhost:5000/companies
Method : GET

# Servicio para obtener una compañía en base al id
http://localhost:5000/company/1
Method : GET

# Servicio para crear una compañía

http://localhost:5000/company/create
Method: POST
Headers: {
    "Content-Type":"application/json"
}
body : {
	"identification":"1231234",
	"name":"Emviame SPA",
	"address": "Manquehue 105, las condes, santiago de chile",
	"mail":"contact@enviame.io",
	"phone":99887766
}
Los datos mail y phone son opcionales

# Servicio para editar una compañía

http://localhost:5000/company/update
Method: PUT
Headers: {
    "Content-Type":"application/json"
}
body : {
	"identification":"1231234",
	"name":"Emviame SPA",
	"address": "Manquehue 105, las condes, santiago de chile",
	"mail":"contact@enviame.io"
}
Los datos son opcionales excepto la identificación

# Servicio para eliminar una compañía

http://localhost:5000/company/delete/1
Method: DELETE
La estructura de la respuesta para todos los servicios es la siguiente

{
    "success": True,
    "message": "Successfully created company",
    "data":{}
}

En caso de error el atributo data no viene en la respuesta.

# Ejercicio 3

http://localhost:5000/scripts/palindrome
Method : GET

Servicio con el cual llamo el script para evaluar los substring palíndromos dentro de la cadena texto dada, en caso de querer probar otra cadena puedes enviar el parámetro "string" con el texto

# Ejercicio 4

http://localhost:5000/scripts/createDelivery
Method : POST

servicio el cual consume servicio de enviame y guarda la respuesta en una tabla log dentro del contenedor mysql

# Ejercicio 5
http://localhost:5000/scripts/DeliveryTime
Method : GET

Servicio con el cual llamo el script para conocer el números de días de entrega de una compra online, basado en la secuencia fibonacci
cada vez que se hace el consumo, se llama el script con un número aleatorio de 0 a 2000, en caso de que se quisiera evaluar una distancia especifica, podrías enviar el parámetro "km" con el número de kilómetros a evaluar.

# Ejercicio 6
http://localhost:5000/scripts/FibonacciDivisors
Method : GET

Servicio con el cual llamo el script para conocer el primer número de la secuencia fibonacci con mas de mil divisores.

En caso de querer probrar con otro límite de divisores enviar el parámetro "divisors"

# Ejercicio 7

Para este ejercicio construí la siguiente query:

SET SQL_SAFE_UPDATES = 0;
update employees 
join countries on countries.id = employees.country_id
join continents on continents.id = countries.continent_id
SET employees.salary = employees.salary + round((continents.anual_adjustment/100) * employees.salary,0)
WHERE employees.salary <= 5000;
SET SQL_SAFE_UPDATES = 0;

Donde se inhabilita el safe_update para ejecutar el update y luego se habilita nuevamente.
