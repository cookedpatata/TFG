document.addEventListener('DOMContentLoaded', () => {

    validarEmail();

    validarPassword();

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