$(document).ready(function(){
    if (window.location.pathname.startsWith("/aparcamientos/")){
        console.log(window.location.pathname)
        initMap();
        $.getJSON(window.location.pathname + '/aparcamiento.json', function(data){
            console.log(data)
            latitud = buscar(data, "latitud");
            longitud = buscar(data, "longitud");
            nombre = buscar(data, "nombre");
            console.log(nombre)
            crearMarcador(nombre, latitud, longitud);
        });
        
    }
});


var initMap = function(){
    //$("#map").fadeIn(800);
    map = L.map('map').setView([40.4175, -3.708], 11);
    L.tileLayer('https://api.tiles.mapbox.com/v4/scarro.0fp5pccj/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic2NhcnJvIiwiYSI6ImNpbmhtdWdnaTAwMmd2ZGx5eHhsaWs5YzEifQ.FONk5Fvpiz12ehN8ByO2GA', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18
    }).addTo(map);
};


function crearMarcador(nombre, lat, lon){
    var marcador = L.marker([lat, lon]);
    marcador.addTo(map).bindPopup(nombre);
    map.setView([lat,lon], 15);
    //marcador.on('popupopen', onPopupOpen);
    existe_marcador = true;
};

function buscar(data,query){
    indice = data.search(query);
    dato = data.slice(indice).split(', ');
    return dato[0].split(': ')[1];
}