$(document).ready(function () {
    let menuAdministracion = $("#administracion");
    let menuGestionPqrs = $("#gestion-pqrs");

    menuAdministracion.on("click", function () {
        $("#opciones-administracion").addClass('show');
    });

    menuGestionPqrs.on("click", function () {
        $("#opciones-pqrs").addClass('show');
    });
});