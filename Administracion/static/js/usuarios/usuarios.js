$(document).ready(function () {
    let estadoMensaje = $("#estadoMensajeEditUsuario").val();
    resaltarOpcionSeleccionadaMenu($("#opciones-administracion"), $("#opcion-usuarios"));

    if (estadoMensaje !== "") {
        if (estadoMensaje === "fallido") {
            showMessage("Edición Fallido!", "No fue posible editar el usuario", "warning");
        } else {
            showMessage("Edición Exitosa!", "La edición del usuario ha sido exitosa", "success");
        }
    }

    $(".swal-button--confirm").click(function () {
        if (estadoMensaje === "exitoso" ) {
            let origin = $(location).attr('origin');
            window.location.href = `${origin}`;
        }
    });
});