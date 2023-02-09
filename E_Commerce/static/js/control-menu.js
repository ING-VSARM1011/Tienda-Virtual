$(document).ready(function () {
    let menuAdministracion = $("#administracion");

    menuAdministracion.on("click", function () {
        $("#opciones-administracion").addClass('show');
    });
});