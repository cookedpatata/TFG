document.addEventListener('DOMContentLoaded', () => {

    const formularios = document.querySelectorAll(
        '.form-apuesta'
    );

    formularios.forEach(form => {

        form.addEventListener('submit', function(e) {

            e.preventDefault();

            const cantidad = form.querySelector(
                'input[name="cantidad"]'
            ).value;

            const confirmar = confirm(
                `¿Confirmar apuesta de ${cantidad} €?`
            );

            if (confirmar) {

                form.submit();

            }

        });

    });

});