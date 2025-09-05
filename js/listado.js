// Espera a que todo el contenido del HTML esté cargado antes de ejecutar el script.
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. BASE DE DATOS DE EJEMPLO ---
    // Como no hay servidor, creamos los datos aquí mismo en un array de objetos.
    const datosAvisos = {
        "1": {
            nombre: "Ana González",
            email: "ana.gonzalez@example.com",
            celular: "+569.11112222",
            comuna: "Providencia",
            descripcion: "Dos gatitos hermanos muy juguetones y cariñosos. Se entregan juntos.",
            fotos: ["https://cataas.com/cat?width=800&height=600", "https://cataas.com/cat?width=800&height=600&r=2"]
        },
        "2": {
            nombre: "Carlos Pérez",
            email: "carlos.perez@example.com",
            celular: "+569.33334444",
            comuna: "Las Condes",
            descripcion: "Perrito mestizo de tamaño mediano, muy activo y leal. Ideal para familias con patio.",
            fotos: ["https://placedog.net/800/600", "https://placedog.net/801/600", "https://placedog.net/802/600"]
        },
        "3": {
            nombre: "María López",
            email: "maria.lopez@example.com",
            celular: "+569.55556666",
            comuna: "Santiago",
            descripcion: "Tiernos gatitos rescatados, buscan un hogar lleno de amor.",
            fotos: ["https://cataas.com/cat?width=800&height=600&r=3"]
        },
        "4": {
            nombre: "Javier Soto",
            email: "javier.soto@example.com",
            celular: "+569.77778888",
            comuna: "Ñuñoa",
            descripcion: "Cachorro juguetón, le encanta correr y jugar a la pelota.",
            fotos: ["https://placedog.net/803/600", "https://placedog.net/804/600"]
        },
        "5": {
            nombre: "Lucía Fernández",
            email: "lucia.fernandez@example.com",
            celular: "+569.99990000",
            comuna: "La Florida",
            descripcion: "Tres cachorros mestizos muy sociables, acostumbrados a estar con niños.",
            fotos: ["https://placedog.net/805/600"]
        }
    };

    // --- 2. SELECCIÓN DE ELEMENTOS DEL DOM ---
    const tablaAvisos = document.getElementById('tabla-avisos').getElementsByTagName('tbody')[0];
    const modalDetalle = document.getElementById('modal-detalle');
    const modalFoto = document.getElementById('modal-foto');
    const cerrarDetalle = document.getElementById('cerrar-detalle');
    const cerrarFoto = document.getElementById('cerrar-foto');
    const fotoGrande = document.getElementById('foto-grande');

    // --- 3. LÓGICA PARA MOSTRAR EL DETALLE ---
    // Agregamos un 'listener' al cuerpo de la tabla.
    tablaAvisos.addEventListener('click', (event) => {
        // Obtenemos la fila (TR) a la que se le hizo clic.
        const fila = event.target.closest('tr');
        if (!fila) return; // Si no se hizo clic en una fila, no hacemos nada.

        const avisoId = fila.dataset.id; // Obtenemos el ID del aviso desde el atributo 'data-id'.
        const datos = datosAvisos[avisoId]; // Buscamos los datos correspondientes.

        if (datos) {
            // Llenamos el modal de detalle con los datos.
            document.getElementById('detalle-nombre').textContent = datos.nombre;
            document.getElementById('detalle-email').textContent = datos.email;
            document.getElementById('detalle-celular').textContent = datos.celular;
            document.getElementById('detalle-comuna').textContent = datos.comuna;
            document.getElementById('detalle-descripcion').textContent = datos.descripcion;

            const galeria = document.getElementById('detalle-fotos');
            galeria.innerHTML = ''; // Limpiamos la galería antes de agregar nuevas fotos.
            
            // Creamos y agregamos las imágenes a la galería.
            datos.fotos.forEach(urlFoto => {
                const img = document.createElement('img');
                img.src = urlFoto;
                img.alt = "Foto de mascota";
                img.addEventListener('click', () => { // A cada foto pequeña le agregamos un listener.
                    fotoGrande.src = urlFoto; // Ponemos su URL en la imagen grande.
                    modalFoto.style.display = 'block'; // Mostramos el modal de la foto grande.
                });
                galeria.appendChild(img);
            });

            modalDetalle.style.display = 'block'; // Mostramos el modal de detalle.
        }
    });

    // --- 4. LÓGICA PARA CERRAR LOS MODALES ---
    // Cerrar el modal de detalle al hacer clic en la 'X'.
    cerrarDetalle.addEventListener('click', () => {
        modalDetalle.style.display = 'none';
    });

    // Cerrar el modal de la foto grande al hacer clic en la 'X'.
    cerrarFoto.addEventListener('click', () => {
        modalFoto.style.display = 'none';
    });

    // Cerrar los modales si se hace clic fuera del contenido.
    window.addEventListener('click', (event) => {
        if (event.target == modalDetalle) {
            modalDetalle.style.display = 'none';
        }
        if (event.target == modalFoto) {
            modalFoto.style.display = 'none';
        }
    });
});