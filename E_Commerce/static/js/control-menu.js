$(document).ready(function () {
    let menuAdministracion = $("#administracion");
    let menuOrdenesCompra = $("#ordenes-compra");

    menuAdministracion.on("click", function () {
        $("#opciones-administracion").addClass('show');
    });

    menuOrdenesCompra.on("click", function () {
        $("#opciones-ordenes").addClass('show');
    });
});