document.addEventListener('DOMContentLoaded', () => {

    validarEmail();

    validarPassword();

    validarNombre();

    validarApellidos();

    validarFecha();

    validarDni();

});

// =====================================
// EMAIL
// =====================================

function validarEmail() {

    const input = document.getElementById('email');

    input.addEventListener('input', () => {

        const regex =
            /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

        mostrarError(
            input,
            !regex.test(input.value),
            'Correo inválido',
            'email-error'
        );

    });

}

// =====================================
// PASSWORD
// =====================================

function validarPassword() {

    const input = document.getElementById('password');

    input.addEventListener('input', () => {

        const valido =
            input.value.length >= 8 &&
            /[A-Z]/.test(input.value) &&
            /\d/.test(input.value);

        mostrarError(
            input,
            !valido,
            '8 caracteres, una mayúscula y un número',
            'password-error'
        );

    });

}

// =====================================
// NOMBRE
// =====================================

function validarNombre() {

    const input = document.getElementById('username');

    input.addEventListener('input', () => {

        mostrarError(
            input,
            input.value.trim().length < 3,
            'Mínimo 3 caracteres',
            'username-error'
        );

    });

}

// =====================================
// APELLIDOS
// =====================================

function validarApellidos() {

    const input = document.getElementById('apellidos');

    input.addEventListener('input', () => {

        mostrarError(
            input,
            input.value.trim().length < 2,
            'Mínimo 2 caracteres',
            'apellidos-error'
        );

    });

}

// =====================================
// FECHA
// =====================================

function validarFecha() {

    const input = document.getElementById('fecha_nac');

    input.addEventListener('change', () => {

        const fecha =
            new Date(input.value);

        const hoy =
            new Date();

        let edad =
            hoy.getFullYear() - fecha.getFullYear();

        const mes =
            hoy.getMonth() - fecha.getMonth();

        if (
            mes < 0 ||
            (
                mes === 0 &&
                hoy.getDate() < fecha.getDate()
            )
        ) {

            edad--;

        }

        mostrarError(
            input,
            edad < 18,
            'Debes ser mayor de edad',
            'fecha-error'
        );

    });

}

// =====================================
// DNI
// =====================================

function validarDni() {

    const input = document.getElementById('dni');

    input.addEventListener('input', () => {

        const regex =
            /^[0-9]{8}[A-Za-z]$/;

        mostrarError(
            input,
            !regex.test(input.value),
            'Formato válido: 12345678A',
            'dni-error'
        );

    });

}

// =====================================
// FUNCION GENERAL
// =====================================

function mostrarError(
    input,
    hayError,
    mensaje,
    errorId
) {

    const error =
        document.getElementById(errorId);

    if (hayError) {

        input.classList.add('input-error');

        error.textContent = mensaje;

    } else {

        input.classList.remove('input-error');

        error.textContent = '';

    }

}