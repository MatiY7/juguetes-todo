# 🧸 ToDo-List de Juguetes  

Aplicación web simple para gestionar tareas relacionadas con juguetes.  

Permite **crear, listar, borrar y marcar como completadas** las tareas.

Proyecto desarrollado para prácticas de programación con Flask + MariaDB.

### FIUBA
### Introduccion al desarollo de software (Lanzillota)

### ✨ Autor
- **Matias You (Padron: 113628)**


### 🧑‍🏫 Corrector
- **Tomás Villegas**

---
---

## 🚀 Tecnologías utilizadas

### 🖥️ Backend
- Python 3  
- Flask  
- MariaDB  

### 🎨 Frontend
- HTML  
- CSS  
- JavaScript

---

## 🗄️ Configuración de la base de datos (MariaDB)

---

```bash 

# Entrar a MariaDB

sudo mysql

# Crear base, usuario y permisos:

CREATE DATABASE juguetes_todo;
CREATE USER 'juguetes_user'@'localhost' IDENTIFIED BY 'mati123';
GRANT ALL PRIVILEGES ON juguetes_todo.* TO 'juguetes_user'@'localhost';
FLUSH PRIVILEGES;

# Crear tablas:

USE juguetes_todo;

CREATE TABLE tareas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT,
  completada BOOLEAN NOT NULL DEFAULT 0
);


# Salir de MariaDB:

EXIT;


```

## 📦 Instalación del proyecto

1️⃣ Activar entorno virtual (si ya existe)
source venv/bin/activate

2️⃣ Instalar dependencias
pip install -r requirements.txt


O manualmente:

pip install flask mariadb

## 🏃‍♂️ Ejecutar el servidor

Con el entorno virtual activo:

python app.py

La aplicación estará disponible en:

👉 http://127.0.0.1:5000/


## 🔁 Endpoints disponibles (API)

#### ✔ GET /tareas

Devuelve todas las tareas.

#### ✔ POST /tareas

Crea una nueva tarea.

Ejemplo JSON:

``` bash

{
  "nombre": "Comprar peluche de oso",
  "descripcion": "Grande y suave"
}

```
#### ✔ DELETE /tareas/<id>

Elimina una tarea por su ID.

#### ✔ PATCH /tareas/<id>/completar

Marca una tarea como completada.

# 🎨 Frontend

### La interfaz se encuentra en:

templates/index.html


### El CSS en:

static/css/style.css


### El JS en:

static/js/app.js

Se comunica con el backend usando fetch().




