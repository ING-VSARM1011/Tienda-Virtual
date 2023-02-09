$(document).ready(function () {
    let iconoArribaPanelResultados = $("#iconoAcordionArribaPanelResultados");
    let iconoAbajoPanelResultados = $("#iconoAcordionAbajoPanelResultados");
    let panelResultados = $("#panel-resultados");
    let opcionesAdministracion = $("#opciones-administracion");
    let opcionProductos = $("#opcion-productos");
    let contenedorTabla = $("#contendor-tabla-productos");

    resaltarOpcionSeleccionadaMenu(opcionesAdministracion, opcionProductos);

    $("#cabecera-panel-resultados").on("click", function () {
        mostrarOcultarIconosAcordionPanel(panelResultados, iconoArribaPanelResultados, iconoAbajoPanelResultados);
    });

    let origin = $(location).attr('origin');
    let url = `${origin}/administracion/productos/index/get-datos`;
    let columnDefs = [
        {className: "dt-control text-center pr-0 mr-0 ml-1 pl-1", "width": "5%", "targets": [0], "visible": true, "searchable": false, "orderable": false},
        {className: "text-center", "targets": [5], "searchable": false, "orderable": false},
        {className: "text-center", "width": "10%", "targets": 1},
        {className: "text-center", "width": "20%", "targets": 2},
        {className: "text-justify", "width": "35%", "targets": 3},
        {className: "text-right", "width": "15%", "targets": 4},
        {className: "text-center", "width": "20%", "targets": 5},
    ]

    panelResultados.addClass("show");
    mostrarElementos([contenedorTabla, iconoArribaPanelResultados]);
    ocultarElementos([iconoAbajoPanelResultados]);

    $("#tablaProductos").DataTable().destroy();

    inicializarDataTable(
        "tablaProductos",
        url,
        columnDefs,
        {}, false
    );
});