const API_URL = "/tareas";

const listaTareasDiv = document.getElementById("listaTareas");
const mensajeVacio = document.getElementById("mensajeVacio");
const inputNombre = document.getElementById("nombre");
const inputDescripcion = document.getElementById("descripcion");
const btnAgregar = document.getElementById("btnAgregar");


document.addEventListener("DOMContentLoaded", cargarTareas);
btnAgregar.addEventListener("click", agregarTarea);


function cargarTareas() {
  fetch(API_URL)
    .then(respuesta => respuesta.json())
    .then(tareas => {
      renderizarTareas(tareas);
    })
    .catch(error => {
      console.error("Error cargando tareas:", error);
      alert("Hubo un problema al cargar las tareas 😢");
    });
}

function renderizarTareas(tareas) {
  listaTareasDiv.innerHTML = "";

  if (tareas.length === 0) {
    mensajeVacio.style.display = "block";
    return;
  } else {
    mensajeVacio.style.display = "none";
  }

  tareas.forEach(tarea => {
    const tareaDiv = document.createElement("div");
    tareaDiv.className = "tarea";
    if (tarea.completada) {
      tareaDiv.classList.add("completada");
    }

    const infoDiv = document.createElement("div");
    infoDiv.className = "tarea-info";
    infoDiv.innerHTML = `
      <strong>${tarea.nombre}</strong><br>
      <small>${tarea.descripcion || ""}</small>
    `;

    const botonesDiv = document.createElement("div");
    botonesDiv.className = "tarea-botones";

    const btnCompletar = document.createElement("button");
    btnCompletar.textContent = "✅ Completar";
    btnCompletar.className = "btn-completar";
    btnCompletar.onclick = () => completarTarea(tarea.id);

    const btnBorrar = document.createElement("button");
    btnBorrar.textContent = "🗑️ Borrar";
    btnBorrar.className = "btn-borrar";
    btnBorrar.onclick = () => borrarTarea(tarea.id);

    botonesDiv.appendChild(btnCompletar);
    botonesDiv.appendChild(btnBorrar);

    tareaDiv.appendChild(infoDiv);
    tareaDiv.appendChild(botonesDiv);

    listaTareasDiv.appendChild(tareaDiv);
  });
}

function agregarTarea() {
  const nombre = inputNombre.value.trim();
  const descripcion = inputDescripcion.value.trim();

  if (!nombre) {
    alert("El nombre de la tarea es obligatorio 😊");
    return;
  }

  const nuevaTarea = { nombre, descripcion };

  fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(nuevaTarea)
  })
    .then(respuesta => respuesta.json())
    .then(tareaCreada => {
      inputNombre.value = "";
      inputDescripcion.value = "";
      cargarTareas(); // recargar la lista
    })
    .catch(error => {
      console.error("Error creando tarea:", error);
      alert("Hubo un problema al crear la tarea 😢");
    });
}


function borrarTarea(id) {
  if (!confirm("¿Seguro que querés borrar esta tarea de juguete?")) {
    return;
  }

  fetch(`${API_URL}/${id}`, {
    method: "DELETE"
  })
    .then(respuesta => respuesta.json())
    .then(resultado => {
      console.log(resultado.mensaje);
      cargarTareas();
    })
    .catch(error => {
      console.error("Error borrando tarea:", error);
      alert("Hubo un problema al borrar la tarea 😢");
    });
}


function completarTarea(id) {
  fetch(`${API_URL}/${id}/completar`, {
    method: "PATCH"
  })
    .then(respuesta => respuesta.json())
    .then(resultado => {
      console.log(resultado.mensaje);
      cargarTareas();
    })
    .catch(error => {
      console.error("Error completando tarea:", error);
      alert("Hubo un problema al completar la tarea 😢");
    });
}
