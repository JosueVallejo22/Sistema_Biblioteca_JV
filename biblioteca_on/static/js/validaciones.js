// Solo aceptar 10 dígitos numéricos para DNI
function validateDNI(input) {
    // Evitar que se escriban letras u otros caracteres no numéricos
    input.addEventListener('keydown', function(event) {
        // Si se presionan teclas que no sean números o teclas de control, las bloqueamos
        if (event.key !== "Backspace" && event.key !== "Delete" &&
            event.key !== "ArrowLeft" && event.key !== "ArrowRight" &&
            event.key !== "Tab" && !/^[0-9]$/.test(event.key)) {
            event.preventDefault(); // Impedir que la tecla se registre
        }
    });

    // Asegurar que solo se ingresen números y validar cédula
    input.addEventListener('input', function() {
        let sanitizedValue = input.value.replace(/[^0-9]/g, ''); // Eliminar todo lo que no sea un número
        if (sanitizedValue.length > 10) {
            sanitizedValue = sanitizedValue.slice(0, 10); // Limitar la longitud a 10 dígitos
        }
        input.value = sanitizedValue; // Asignar el valor limpio y validado

        // Validación de la cédula ecuatoriana
        if (sanitizedValue.length === 10) {
            let suma = 0;
            for (let i = 0; i < sanitizedValue.length - 1; i++) {
                let x = parseInt(sanitizedValue[i]);
                if (i % 2 === 0) {
                    x = x * 2;
                    if (x > 9) {
                        x = x - 9;
                    }
                }
                suma += x;
            }

            let modulo = suma % 10;
            let result = modulo === 0 ? 0 : 10 - modulo;
            let ultimoDigito = parseInt(sanitizedValue[9]);

            // Mostrar mensaje si no es válido
            if (result !== ultimoDigito) {
                // Aquí, puedes modificarlo para mostrar un mensaje de error en el HTML
                console.log("La cédula no es ecuatoriana");
                input.setCustomValidity("La cédula no es válida"); // Para mensajes de error en el formulario
            } else {
                console.log("La cédula es ecuatoriana");
                input.setCustomValidity(""); // Limpiar el mensaje de error
            }
        }
    });
}

// Para el teléfono, similar
function validatePhoneNumber(input) {
    input.addEventListener('keydown', function(event) {
        if (event.key !== "Backspace" && event.key !== "Delete" &&
            event.key !== "ArrowLeft" && event.key !== "ArrowRight" &&
            event.key !== "Tab" && !/^[0-9]$/.test(event.key)) {
            event.preventDefault(); // Bloquear la tecla si no es un número
        }
    });

    input.addEventListener('input', function() {
        let sanitizedValue = input.value.replace(/[^0-9]/g, ''); // Eliminar no-números
        if (sanitizedValue.length > 10) {
            sanitizedValue = sanitizedValue.slice(0, 10); // Limitar a 10 dígitos
        }
        input.value = sanitizedValue;
    });
}
