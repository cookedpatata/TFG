document.addEventListener('DOMContentLoaded', () => {

    const formularios = document.querySelectorAll(
        '.form-apuesta'
    );

    // =========================================
    // CREAR POPUP
    // =========================================

    const overlay = document.createElement('div');
    overlay.className = 'popup-overlay';

    overlay.innerHTML = `
        <div class="popup-confirmacion">
            <h2>Confirm Bet</h2>

            <p id="popup-texto"></p>

            <div class="popup-botones">
                <button id="cancelar-popup" class="btn-cancelar">
                    Cancel
                </button>

                <button id="confirmar-popup" class="btn-confirmar">
                    Confirm
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);

    const textoPopup = document.getElementById(
        'popup-texto'
    );

    const btnCancelar = document.getElementById(
        'cancelar-popup'
    );

    const btnConfirmar = document.getElementById(
        'confirmar-popup'
    );

    let formularioActual = null;

    formularios.forEach(form => {

        form.addEventListener('submit', function(e) {

            e.preventDefault();

            const cantidad = form.querySelector(
                'input[name="cantidad"]'
            ).value;

            textoPopup.textContent =
                `Are you sure you want to bet ${cantidad} €?`;

            formularioActual = form;

            overlay.classList.add('activo');

        });

    });

    btnCancelar.addEventListener('click', () => {

        overlay.classList.remove('activo');

    });

    btnConfirmar.addEventListener('click', () => {

        if (formularioActual) {

            formularioActual.submit();

        }

    });

});