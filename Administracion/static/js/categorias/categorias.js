$(document).ready(function () {
    let iconoArribaPanelResultados = $("#iconoAcordionArribaPanelResultados");
    let iconoAbajoPanelResultados = $("#iconoAcordionAbajoPanelResultados");
    let panelResultados = $("#panel-resultados");
    let opcionesAdministracion = $("#opciones-administracion");
    let opcionCategorias = $("#opcion-categoria");
    let contenedorTabla = $("#contendor-tabla-categorias");

    resaltarOpcionSeleccionadaMenu(opcionesAdministracion, opcionCategorias);

    $("#cabecera-panel-resultados").on("click", function () {
        mostrarOcultarIconosAcordionPanel(panelResultados, iconoArribaPanelResultados, iconoAbajoPanelResultados);
    });

    let origin = $(location).attr('origin');
    let url = `${origin}/administracion/categorias/index/get-datos`;
    let columnDefs = [
        {className: "dt-control text-center pr-0 mr-0 ml-1 pl-1", "width": "5%", "targets": [0], "visible": true, "searchable": false, "orderable": false},
        {className: "text-center", "targets": [4], "searchable": false, "orderable": false},
        {className: "text-center", "width": "20%", "targets": 1},
        {className: "text-justify", "width": "35%", "targets": 2},
        {className: "text-center", "width": "15%", "targets": 3},
        {className: "text-center", "width": "20%", "targets": 4},
    ]

    panelResultados.addClass("show");
    mostrarElementos([contenedorTabla, iconoArribaPanelResultados]);
    ocultarElementos([iconoAbajoPanelResultados]);

    $("#tablaCategorias").DataTable().destroy();

    inicializarDataTable(
        "tablaCategorias",
        url,
        columnDefs,
        {}, true
    );
});