# X-Serv-Practica-Aparcamientos
Repositorio de inicio de la práctica final - Curso 2016/2017

<h2>Autor: Sergio Carro Albarrán </h2>
<h2>Titulación: ITT </h2>
<h3>Github: scarro</h3>
<br/>
<h2>Funcionamiento:</h2>

<p>La aplicación de aparcamientos diseñada toma los datos de todos los aparcamientos registrados en la web del municipio de madrid y muestra sus carácteristicas así como algunas opciones dependiendo de si se está registrado o no.</p>

<p>Una vez cargada la base de datos, el usuario autenticado o no, podrá ver cada uno de los aparcamientos de la comunidad y filtrarlos por distrito. También podŕá entrar en páginas de usuarios ya registrados y ver su selección personal de aparcamientos, así como dar puntuación a cada uno de ellos.</p>
<p>Si se ha registrado en la página además podrá seleccionar un aparcamiento para añadirlo a su lista, comentar sobre cada uno de ellos, así como cambiar el título de su página o el color y el tamaño con el que se le muestra la página.</p>
<p>Además se dispone de un botón para mostrar en cualquier momento los aparcamientos con accesibilidad disponibles.</h2>
<h2>Peculiaridades:</h2>
<ul>
    <li>Para desarrollar el aspecto de la página se ha utilizado en gran medida bootstrap 4, aunque algunas características han necesitado de un css propio. Por ello la página es lo más responsive que he podido.</li>
    <li>La accesibilidad de cada aparcamiento se muestra con un icono.</li>
    <li>En la página principal, se muestran en un badge gris el número de comentarios que tiene un aparcamiento y, si alguno tiene "me gusta" se muestra su número en un badge verde. También se muestran en un badge rojo al lado del nombre de cada página de usuario, el número de aparcamientos seleccionados.</li>
    <li>Es posible anular la selección de un aparcamiento</li>
</ul>
<h2>Funcionalidades opcionales:</h2>
<ol>
    <li>Se ha incluido el favicon del sitio</li>
    <li>Genera XML para los contenidos de la página principal</li>
    <li>Genera JSON para los contenidos de la página principal</li>
    <li>Es posible el registro de usuarios</li>
    <li>Para mostrar las coordenadas de cada aparcamiento se solicita al servidor, mediante una petición AJAX, el json de cada aparcamiento, y una vez procesado se crea el marcador que se pone sobre el mapa, todo ello usando javascript. </li>
    <li>Se puede puntuar con "+1" o "Me gusta" a cada aparcamiento (y se muestra el número total de los mismos)</li>
</ol>
<h2>Vídeo demostración:</h2>
<p>Parte básica:</p>
<p>Parte optativa:</p>