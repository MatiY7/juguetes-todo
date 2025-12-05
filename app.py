from flask import Flask, request, jsonify, render_template
import mariadb

app = Flask(__name__)


DB_CONFIG = {
    "host": "localhost",
    "user": "juguetes_user",       
    "password": "mati123",         
    "database": "juguetes_todo",   
    "port": 3306
}


def get_connection():
    """Crea y devuelve una conexión a la base de datos MariaDB."""
    try:
        conn = mariadb.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"],
        )
        return conn
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return None




@app.get("/")
def home():
    """Devuelve la página HTML principal de la ToDo List."""
    return render_template("index.html")

# 📥 GET /tareas -> lista todas las tareas
@app.get("/tareas")
def obtener_tareas():
    conn = get_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cur = conn.cursor()
    cur.execute("SELECT id, nombre, descripcion, completada FROM tareas;")
    filas = cur.fetchall()

    tareas = []
    for fila in filas:
        tareas.append({
            "id": fila[0],
            "nombre": fila[1],
            "descripcion": fila[2],
            "completada": bool(fila[3]),
        })

    cur.close()
    conn.close()

    return jsonify(tareas), 200



@app.post("/tareas")
def crear_tarea():
    data = request.get_json()

    if not data:
        return jsonify({"mensaje": "Falta cuerpo JSON"}), 400

    nombre = data.get("nombre")
    descripcion = data.get("descripcion", "")

    if not nombre:
        return jsonify({"mensaje": "El campo 'nombre' es obligatorio"}), 400

    conn = get_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO tareas (nombre, descripcion, completada) VALUES (?, ?, ?);",
            (nombre, descripcion, 0)
        )
        conn.commit()
        nuevo_id = cur.lastrowid

    except mariadb.Error as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"mensaje": f"Error al crear la tarea: {e}"}), 500

    cur.close()
    conn.close()

    nueva_tarea = {
        "id": nuevo_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "completada": False,
    }

    return jsonify(nueva_tarea), 201



@app.delete("/tareas/<int:id>")
def borrar_tarea(id):
    conn = get_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM tareas WHERE id = ?;", (id,))
        conn.commit()

        if cur.rowcount == 0:
            mensaje = f"No existe la tarea con id {id}"
            status = 404
        else:
            mensaje = f"Tarea {id} borrada correctamente"
            status = 200

    except mariadb.Error as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"mensaje": f"Error al borrar la tarea: {e}"}), 500

    cur.close()
    conn.close()

    return jsonify({"mensaje": mensaje}), status


@app.patch("/tareas/<int:id>/completar")
def completar_tarea(id):
    conn = get_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cur = conn.cursor()

    try:
        cur.execute("UPDATE tareas SET completada = 1 WHERE id = ?;", (id,))
        conn.commit()

        if cur.rowcount == 0:
            mensaje = f"No existe la tarea con id {id}"
            status = 404
        else:
            mensaje = f"Tarea {id} marcada como completada"
            status = 200

    except mariadb.Error as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"mensaje": f"Error al actualizar la tarea: {e}"}), 500

    cur.close()
    conn.close()

    return jsonify({"mensaje": mensaje}), status



if __name__ == "__main__":
    app.run(debug=True)

