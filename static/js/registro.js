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
            'Invalid email',
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
            '8 characters, one uppercase letter and one number',
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
            'Minimum 3 characters',
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
            'Minimum 2 characters',
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
            'You must be of legal age',
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
            'Valid format: 12345678A',
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