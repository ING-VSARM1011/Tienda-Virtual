$(document).ready(function () {
    let iconoArribaPanelResultados = $("#iconoAcordionArribaPanelResultados");
    let iconoAbajoPanelResultados = $("#iconoAcordionAbajoPanelResultados");
    let panelResultados = $("#panel-resultados");
    let opcionesOrdenes = $("#opciones-ordenes");
    let opcionOrdenes = $("#opcion-mis-ordenes");
    let contenedorTabla = $("#contendor-tabla-ordenes");

    resaltarOpcionSeleccionadaMenu(opcionesOrdenes, opcionOrdenes);

    $("#cabecera-panel-resultados").on("click", function () {
        mostrarOcultarIconosAcordionPanel(panelResultados, iconoArribaPanelResultados, iconoAbajoPanelResultados);
    });

    let origin = $(location).attr('origin');
    let url = `${origin}/ordenes-compra/mis-ordenes/index/get-datos`;
    let columnDefs = [
        {className: "dt-control text-center", "width": "5%", "targets": [0], "visible": true, "searchable": false, "orderable": false},
        {className: "text-center", "targets": [5], "searchable": false, "orderable": false},
        {className: "text-center", "width": "12%", "targets": 1},
        {className: "text-center", "width": "12%", "targets": 2},
        {className: "text-justify", "width": "35%", "targets": 3},
        {className: "text-center", "width": "21%", "targets": 4},
        {className: "text-center", "width": "20%", "targets": 5},
    ]

    panelResultados.addClass("show");
    mostrarElementos([contenedorTabla, iconoArribaPanelResultados]);
    ocultarElementos([iconoAbajoPanelResultados]);

    $("#tablaOrdenes").DataTable().destroy();

    inicializarDataTable(
        "tablaOrdenes",
        url,
        columnDefs,
        {}, false
    );
});