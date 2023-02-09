$(document).ready(function () {
    let estadoMensaje = $("#estadoMensaje").val();

    if (estadoMensaje !== "") {
        if (estadoMensaje === "fallido") {
            showMessage("Registro Fallido!", "El correo electrónico ingresado no es valido.", "warning");
        } else {
            showMessage("Registro Exitoso!", "El registro ha sido exitoso. Ya tiene acceso a la plataforma", "success");
        }
    }

    $(".swal-button--confirm").click(function () {
        if (estadoMensaje === "exitoso" ) {
            let origin = $(location).attr('origin');
            window.location.href = `${origin}`;
        }
    });

    validarFormularioEnvio($("#registrarse-form"));
});