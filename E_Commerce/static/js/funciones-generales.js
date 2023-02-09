/**
 * Implementación general de AJAX que espera respuesta en JSON con el formato estándar definido en EVA.
 * @param url String con la url a donde se envia el formulario.
 * @param datos Datos a enviar, en el caso de el método ser diferente de "get" se envira como un string JSON.
 * @param metodo Método http a utilizar, get, post, put, delete, etc.
 * @param menEnvio Mensaje que se desea mostrar durante el envío y mientras se recibe respuesta.
 * @param menError Mensaje que se desea mostrar en caso de que ocurra un error en la comunicación.
 * @returns {Promise<Promise|*>} Promesa que se resuelve con los datos contenidos es la respuesta  o se rechaza con los
 * datos también si la respuesta indica que es un error pero si es un error de ajax se rechaza con null.
 */
 async function envioAjax(url, datos, metodo, menEnvio='', menError='') {
  try {

      const resp = await $.ajax({
          url: url,
          type: metodo,
          data: metodo ==='get' ? datos : JSON.stringify(datos),
          cache: false,
          processData: true,
          contentType: metodo === 'get' ? 'application/x-www-form-urlencoded' : "application/json; charset=utf-8;",
          dataType: "json",
          beforeSend: metodo ==='get' ? '': function(xhr) {xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'))
          },
      });

      if (resp.estado === 'OK') {
          if(resp.mensaje)
            showMessage("Exitoso!", resp.mensaje, "success");
          return resp.datos;
      } else {
          resp.estado === 'error' ?
            showMessage("Error!", resp.mensaje, "error") :
            showMessage("Error!", "Ha ocurrido un error al consultar la información, contacte a soporte", "error");
          return Promise.reject(resp.datos);
      }
  } catch (e) {
      console.error(e);
      showMessage("Error!", "Error inesperado", "error");
      return Promise.reject(null);
  } finally {
    //showMessage("Error!", "Error inesperado", "error");
  }
}

/**
* Implementación general de AJAX para post que espera respuesta en JSON con el formato estándar definido en EVA y
* envia los datos como un string JSON.
* @param url String con la url a donde se envia el formulario.
* @param datos Datos a enviar.
* @param menEnvio Mensaje que se desea mostrar durante el envío y mientras se recibe respuesta.
* @param menError Mensaje que se desea mostrar en caso de que ocurra un error en la comunicación.
* @returns {Promise<Promise|*>} Promesa que se resuelve con los datos contenidos es la respuesta  o se rechaza con los
* datos también si la respuesta indica que es un error pero si es un error de ajax se rechaza con null.
*/
async function postAjax(url, datos, menEnvio, menError) {
 return envioAjax(url, datos, 'post', menEnvio, menError);
}

/**
* Implementación general de AJAX para get que espera respuesta en JSON con el formato estándar definido en EVA.
* @param url String con la url a donde se envia el formulario.
* @param datos Datos a enviar
* @param menEnvio Mensaje que se desea mostrar durante el envío y mientras se recibe respuesta.
* @param menError Mensaje que se desea mostrar en caso de que ocurra un error en la comunicación.
* @returns {Promise<Promise|*>} Promesa que se resuelve con los datos contenidos es la respuesta  o se rechaza con los
* datos también si la respuesta indica que es un error pero si es un error de ajax se rechaza con null.
*/
async function getAjax(url, datos, menEnvio, menError) {
 return envioAjax(url, datos, 'get', menEnvio, menError);
}

/**
* Muestra un modal en pantalla del tipo SweetAlert de acuerdo a los parametro pasados.
* @param titulo titulo que se mostrara.
* @param mensaje mensaje que se mostrara.
* @param icono Tipo de icono que indicara el tipo de mensaje.
* Ejm: "success" es exitoso, "warning" es advertencia, "error" es error, "info" es informativo.
*/
function showMessage(titulo, mensaje, icono) {
  swal({
    title: titulo,
    text: mensaje,
    type: icono,
    confirmButtonText: 'Aceptar',
  });
  $(".swal-text").addClass('text-center');
}

/**
* Se elimina el elemento referenciado, mostrando mensaje exitoso y cargando porsteriormente la página de donde se elimino.
 * @param pathModulo ruta que hace refencia al módulo de donde se esta eliminando el elemento.
 * @param idElemento id del elemento que se desea eliminar.
 * @param nombre nombre del elemento que se desea eliminar.
*/
function eliminarElemento(pathModulo, nombre, idElemento) {
    swal({
        title: `¿Desea Eliminar ${nombre}?`,
        text: `Por favor, escriba un motivo y confirme la eliminación`,
        imageUrl: '../../static/assets/img/icono-eliminar.png',
        input: "text",
        showCancelButton: true,
        confirmButtonText: "Confirmar",
        cancelButtonText: "Cancelar",
        padding: '2em',
        inputValidator: motivo => {
            // Si el valor es válido, debes regresar undefined. Si no, una cadena
            if (!motivo) {
                return "Por favor escriba un motivo de eliminación";
            } else {
                return undefined;
            }
        }
    }).then(resultado => {
        if (resultado.value) {
            let motivoEliminacion = resultado.value;
            let origin = $(location).attr('origin');
            let datos = {motivo: motivoEliminacion}
            getAjax(`${origin}${pathModulo}${idElemento}/eliminar`, datos).then((json) => {
                if (json) {
                    showMessage(json.titulo, json.mensaje, json.icono);
                    $(".swal2-confirm").on("click", function () {
                        window.location.href = `${origin}${json.ruta}`;
                    });
                }
            });
        }
    });
}

/**
* Se elimina el usuario referenciado, mostrando mensaje exitoso y redirigiendo al inicio de sesión de la plataforma.
 * @param pathModulo ruta que hace refencia al módulo de donde se esta eliminando el elemento.
 * @param idElemento id del elemento que se desea eliminar.
 * @param nombre nombre del elemento que se desea eliminar.
 * @param campo campo de referencia del elemento que se desea eliminar.
 * @param referencia código o valor de referencia del elemento que se desea eliminar.
*/
function eliminarUsuario(pathModulo, nombre, campo, referencia, idElemento) {
    swal({
        title: `¿Desea Eliminar ${nombre}?`,
        text: `Por favor, confirme la eliminación del ${nombre} con ${campo}: ${referencia}`,
        imageUrl: '../../static/assets/img/icono-eliminar.png',
        showCancelButton: true,
        confirmButtonText: "Confirmar",
        cancelButtonText: "Cancelar",
        padding: '2em',
    }).then(resultado => {
        if (resultado.value) {
            let origin = $(location).attr('origin');
            getAjax(`${origin}${pathModulo}${idElemento}/eliminar`).then((json) => {
                if (json) {
                    showMessage(json.titulo, json.mensaje, json.icono);
                    $(".swal2-confirm").on("click", function () {
                        let origin = $(location).attr('origin');
                        console.log(json.ruta);
                        if (json.ruta === '') {
                            window.location.href = `${origin}`;
                        } else {
                            window.location.href = `${origin}${json.ruta}`;
                        }
                    });
                }
            });
        }
    });
}

/**
* Muestra los elementos pasados en el arreglo.
* @param idsElementos arreglo con los elementos que se desean mostrar.
*/
function mostrarElementos(idsElementos) {
    idsElementos.map(elem => {
        elem.removeAttr("hidden");
    });
}

/**
* oculta los elementos pasados en el arreglo.
* @param idsElementos arreglo con los elementos que se desean ocultar.
*/
function ocultarElementos(idsElementos) {
    idsElementos.map(elem => {
        elem.attr("hidden", true);
    });
}

/**
* Agrega la clase de requerido a los elementos pasados en el arreglo.
* @param idsElementos arreglo con los elementos a los cuales se les desea agregar la clase de requerido.
*/
function agregarRequiredElementos(idsElementos) {
    idsElementos.map(elem => {
        elem.attr("required", true);
    });
}

/**
* Quita la clase de requerido a los elementos pasados en el arreglo.
* @param idsElementos arreglo con los elementos a los cuales se les desea quitar la clase de requerido.
*/
function quitarRequiredElementos(idsElementos) {
    idsElementos.map(elem => {
        elem.removeAttr("required");
    });
}

/**
* Valida que el formulario tenga todos los campos requeridos completos para realizar el envio(submit), de no ser asi,
 * activa las validaciones de los campos incompletos para indicarle al usuario que debe completarlos.
* @param form formulario al cual se le desea verificar las validaciones de los campos.
*/
function validarFormularioEnvio(form) {
    (function () {
        form.on("submit", function (e) {
            e.preventDefault();
            if (!form[0].checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                form[0].classList.add("was-validated");
            } else {
                form[0].submit();
            }
        });
    })();
}

/**
 * Aplica dataTable a la tabla pasada como parametro.
 * @param idTabla Id de la tabla donde se desea aplicar el dataTable.
 * @param url Ruta de donde se van a obtener los datos de la tabla.
 * @param colDefs Arreglo con la definición del ancho de las columnas.
 * Ejm. [{ "width": "10%", "targets": 0 }, { "width": "25%", "targets": 1},..]
 * @param dataAjax objeto que indica las llaves-valor con la información de los filtros seleccionados o digitados
 * por el usuario.
 * @param inputBusqueda booleano que indica si se habilita el input de búsqueda en el dataTable.
 * @param orden Arreglo de arreglos con la posicion de las columna y el orden
 * jerargico como se quiere ordenar la tabla. Ejm. [[1, 'asc'], [2, 'desc]]
 * Los nombres se deben pasar exactamente como se definierón en las llaves de los
 * objetos (información) en los datos.
 */
function inicializarDataTable(idTabla, url, colDefs, dataAjax, inputBusqueda, orden) {
    $(`#${idTabla}`).DataTable({
        dom: "<'dt--top-section'<'row'<'col-12 col-sm-6 d-flex justify-content-sm-start justify-content-center'l><'col-12 col-sm-6 d-flex justify-content-sm-end justify-content-center mt-sm-0 mt-3'f>>>" +
             "<'table-responsive'tr>" +
             "<'dt--bottom-section d-sm-flex justify-content-sm-between text-center'<'dt--pages-count  mb-sm-0 mb-3'i><'dt--pagination'p>>",
        processing: true,
        serverSide: true,
        responsive: true,
        columnDefs: colDefs,
        searching: inputBusqueda,
        order: orden,
        PaginationType: 'full_numbers',
        LengthMenu: [[10, 25, 50], [10, 25, 50]],
        pageLength: 10,
        language: {
          url: "https://cdn.datatables.net/plug-ins/1.12.1/i18n/es-ES.json",
          infoFiltered: ""
        },
        ajax: {
            url: url,
            type: 'post',
            data: dataAjax,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'))
            },
            dataType: "json",
            error: function (e) {
                console.log(e);
            }
        }
    });
}

/**
* Mantiene desplagadas las opciones del menú y resalta la opción que se ha seleccionado y que dirige al template que se
 * esta visualizando.
* @param idOpcionesMenu id del contender que abarca las opciones del menú.
 * @param idOpcion id de la opción seleccionada del menú.
*/
function resaltarOpcionSeleccionadaMenu(idOpcionesMenu, idOpcion) {
    idOpcionesMenu.addClass('show');
    idOpcion.addClass('active');
}


/**
* Muestra y oculta los iconos de arriba y abajo de la cabecera del panel de acuerdo a si la información del panel
 * esta desplegada o no.
 * @param idPanel id del panel cabecera.
 * @param idIconoArriba id del icono arriba.
 * @param idIconoAbajo id de del icono abajo.
*/
function mostrarOcultarIconosAcordionPanel(idPanel, idIconoArriba, idIconoAbajo) {
    let PanelResultados = idPanel;
    let iconoAcordionArriba = idIconoArriba;
    let iconoAcordionAbajo = idIconoAbajo;
    if (PanelResultados.hasClass('show')) {
        mostrarElementos([iconoAcordionAbajo]);
        ocultarElementos([iconoAcordionArriba]);
    } else {
        mostrarElementos([iconoAcordionArriba]);
        ocultarElementos([iconoAcordionAbajo]);
    }
}

/**
* Limpia los valores ingresados en los inputs pasados en el arreglo, volviendo a mostrar el placeholder.
 * @param inputs array con los ids de los inputs que se desean restablecer.
*/
function restablecerInputs(inputs) {
    inputs.map(input => {
        input.val('');
    });
}

/**
* Limpia los valores seleccionados en los selects pasados en el arreglo, volviendo a mostrar valor por defecto.
 * @param selects array con los ids de los selects que se desean restablecer.
*/
function restablecerSelects(selects) {
    selects.map(select => {
        select.val("").trigger("change");
    });
}

function abrirModal(url, idModal, idForm) {
    $(`#${idModal}`).load(url, function () {
       $(this).modal("show");
       validarFormularioEnvio($(`#${idForm}`));
       new TomSelect("#select-state",{
            maxItems: 10
        });
    });
}