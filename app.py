from flask import Flask
from flask import render_template, request, redirect, session
from flask_mysqldb import MySQL
from datetime import datetime
from flask import send_from_directory
from datetime import timedelta
from flask import session, redirect, url_for
from functools import wraps
import os
app=Flask(__name__)
app.secret_key="omarwebtech"
mysql=MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'barberiamacha'
mysql.init_app(app)
#login autentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('cliente_login'))
        return f(*args, **kwargs)
    return decorated_function
# login fin
# Ruta para mostrar el formulario de citas
@app.route('/cita/crear', methods=['GET'])
@login_required
def mostrar_formulario_cita():
    # Obtener lista de barberos para el desplegable
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario, nombre, apellido FROM usuario WHERE rol = 'barbero'")
    barberos = cursor.fetchall()
    conexion.commit()
    cursor.close()
    return render_template('sitio/hacer_cita.html', barberos=barberos)
# Ruta para procesar el formulario de citas
@app.route('/cita/crear', methods=['POST'])
@login_required
def hacer_cita():
    if request.method == 'POST':
        fecha = request.form['fecha']
        hora = request.form['hora']
        nota = request.form['nota']
        estado = 'pendiente'  # Por defecto
        id_cliente = session['usuario_id']
        # Verificar si 'barbero' está presente en el formulario
        if 'barbero' not in request.form:
            return "Error: El campo 'barbero' no está presente en el formulario."
        id_barbero = request.form['barbero']
        # conexion = mysql.connection
        # cursor = conexion.cursor()
        # cursor.execute("INSERT INTO citas (fecha, hora, nota, estado, id_cliente, id_barbero) VALUES (%s, %s, %s, %s, %s, %s)",
        #                (fecha, hora, nota, estado, id_cliente, id_barbero))
        # conexion.commit()
        # cursor.close()
        # return redirect(url_for('cita'))
        try:
            conexion = mysql.connection
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO citas (fecha, hora, nota, estado, id_cliente, id_barbero) VALUES (%s, %s, %s, %s, %s, %s)",
                           (fecha, hora, nota, estado, id_cliente, id_barbero))
            conexion.commit()
            cursor.close()
            return redirect(url_for('mis_citas'))
        except Exception as e:
            return f"Error al crear la cita: {str(e)}"

# @app.route('/mis_citas')
# def citas_mias():
#     return render_template('sitio/mis_citas.html')

@app.route('/mis_citas')
@login_required
def mis_citas():
    # Obtener el ID del usuario actual
    usuario_id = session['usuario_id']
    # Consultar las citas individuales del usuario actual
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT c.id_cita, c.fecha, c.hora, c.nota, c.estado,
               u_barbero.nombre AS nombre_barbero, u_barbero.apellido AS apellido_barbero, p.corteRealizado
        FROM citas c
        JOIN usuario u_barbero ON c.id_barbero = u_barbero.id_usuario
        LEFT JOIN pagos p ON c.id_cita = p.id_cita
        WHERE c.id_cliente = %s
    """, (usuario_id,))
    citas = cursor.fetchall()
    print(citas)
    conexion.commit()
    cursor.close()
    return render_template('sitio/mis_citas.html', citas=citas)
@app.route('/')
@login_required
def inicio():
    return render_template('sitio/index.html')
# registar el clinete 
@app.route('/cliente/registro')
def registro_cliente():
    return render_template('sitio/cliente_registro.html')
@app.route('/cliente/registro', methods=['POST'])
def cliente_registro():
    if request.method == 'POST':
        # Obtener los datos del formulario
        tipo_documento = request.form['tipo_documento']
        numero_documento = request.form['numero_documento']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        celular = request.form['celular']
        email = request.form['email']
        password = request.form['password']
        # Insertar los datos en la base de datos
        conn = mysql.connection
        cursor = conn.cursor()
        query = "INSERT INTO usuario (tipoDeDocumento, numeroDeDocumento, nombre, apellido, celular, email, password, rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (tipo_documento, numero_documento, nombre, apellido, celular, email, password, 'cliente'))
        conn.commit()
        cursor.close()
        # Redirigir a la página de inicio de sesión
        return redirect(url_for('cliente_login'))
@app.route('/cliente/login')
def login_cliente():
    return render_template('sitio/login.html')
# inicio de seccion del cliente 
@app.route('/cliente/login', methods=['POST'])
def cliente_login():
    if request.method == 'POST':
        email = request.form['email_cliente']
        password = request.form['password_cliente']
        conn = mysql.connection
        cursor = conn.cursor()
        query = "SELECT id_usuario FROM usuario WHERE email = %s AND password = %s AND rol = 'cliente'"
        cursor.execute(query, (email, password))
        usuario = cursor.fetchone()
        cursor.close()
        if usuario:
            session['usuario_id'] = usuario[0]  # Almacenar el ID del usuario en la sesión
            print("ID del usuario en sesión:", session['usuario_id'])  # Imprimir el ID del usuario en la consola
            return redirect(url_for('mis_citas'))  # Redirigir a la página de citas o donde sea necesario
        else:
            # Mensaje de error o redireccionamiento a la página de inicio de sesión nuevamente
            return render_template('sitio/login.html', mensaje="Credenciales incorrectas. Inténtalo de nuevo.")
        # etc 
@app.route('/img/barberia/logo/')
def logo_barberia():
    return send_from_directory('templates/sitio/IMG_BARBERIA', 'barbero1.jpg')
# rutas 
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)
@app.route('/css/<archivocss>')
def css_Link(archivocss):
    # print(archivocss)
    return send_from_directory(os.path.join('templates/sitio/css'),archivocss)
# @app.route('/cita')
# def cita():
#     conexion=mysql.connection
#     cursor=conexion.cursor()
#     cursor.execute("SELECT * FROM citas")
#     citas=cursor.fetchall()
#     conexion.commit()
#     # print(cita)
#     return render_template('sitio/citas.html', citas=citas)

@app.route('/nosotros')
@login_required
def nosotros():
    return render_template('sitio/nosotros.html')
# secccion de admin 
@app.route('/admin/') # decorador de una ruta en flask
def admin_index():
    # Cuando un usuario realiza una solicitud a la ruta /admin/, Flask llama a la función admin_index(). Dentro de la función, primero verifica si la clave 'login' no está presente en la sesión del usuario utilizando la expresión not 'login' in session. Esto significa que si el usuario no ha iniciado sesión (la clave 'login' no está presente en la sesión), se redirige al usuario a la página de inicio de sesión en /admin/login.
    if not 'login' in session: # Aquí se verifica si la clave 'login' no está presente en la sesión del usuario. La sesión es un lugar donde se puede almacenar información para mantenerla entre diferentes solicitudes del mismo usuario. Si 'login' no está en la sesión, significa que el usuario no ha iniciado sesión.
        return redirect("/admin/login")
    return render_template('admin/index.html')
#En resumen, la función admin_index() garantiza que solo los usuarios que hayan iniciado sesión puedan acceder al área de administración. Si un usuario intenta acceder a /admin/ sin haber iniciado sesión, será redirigido a la página de inicio de sesión. Esto proporciona seguridad y control de acceso a las áreas protegidas de la aplicación.
@app.route('/admin/login')
def admin_login():
    return render_template('admin/loguin.html')
@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _email = request.form['txtEmail']
    _password = request.form['txtPassword']
    # Conectar a la base de datos
    conn = mysql.connection
    cursor = conn.cursor()
    # Consulta SQL para verificar las credenciales del usuario
    query = "SELECT id_usuario, rol, nombre, apellido FROM usuario WHERE email = %s AND password = %s"
    cursor.execute(query, (_email, _password))
    usuario = cursor.fetchone()  # Obtener el primer registro que coincida con las credenciales
    # Cerrar la conexión
    cursor.close()
    if usuario and usuario[1] == 'admin':  # Si el usuario existe y tiene el rol de administrador
        session["login"] = True
        session["usuario"] = "Administrador"
        # Imprimir los detalles del usuario por consola
        print("Administrador conectado:")
        print("ID de usuario:", usuario[0])
        print("Nombre:", usuario[2])
        print("Apellido:", usuario[3])
        return redirect("/admin")
    else:
        return render_template('admin/loguin.html', mensaje="Acceso Denegado 🤖🤷‍♀️⬆️➡️ sigue intentando xdddd!!")
@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    print("Cerrando Seccion Exitosamente . 💈")
    return render_template('admin/loguin.html')
# @app.route('/admin/cerrar')
# def admin_login_cerrar():
#     if 'usuario_id' in session:
#         usuario_id = session['usuario_id']
#         session.clear()
#         print(f"Administrador con ID {usuario_id} desconectado.")
#     else:
#         print("No hay administrador conectado.")
#     return render_template('admin/loguin.html')

@app.route('/admin/citas')
def admin_citas():
    if not 'login' in session:
        return redirect("/admin/login")
    # Obtener los datos de las citas con los detalles del cliente y el barbero
    conexion = mysql.connection
    # cursor = conexion.cursor(dictionary=True)
    cursor = conexion.cursor()
    cursor.execute("""
SELECT c.id_cita, c.fecha, c.hora, c.nota, c.estado,
       u_cliente.nombre AS nombre_cliente, u_cliente.apellido AS apellido_cliente, u_cliente.numeroDeDocumento AS dni_cliente, u_cliente.celular AS celular_cliente,
       u_barbero.nombre AS nombre_barbero, u_barbero.apellido AS apellido_barbero, u_barbero.numeroDeDocumento AS dni_barbero
FROM citas c
JOIN usuario u_cliente ON c.id_cliente = u_cliente.id_usuario
JOIN usuario u_barbero ON c.id_barbero = u_barbero.id_usuario;
    """)
    citas = cursor.fetchall()
    conexion.commit()
    # cursor.close()
    print(citas)
    return render_template('admin/citas.html', citas=citas)

# poder modificar el estado de cita 
@app.route('/admin/cita/<int:cita_id>/editar', methods=['POST'])
def editar_estado_cita(cita_id):
    if request.method == 'POST':
        nuevo_estado = request.form['estado']
        # Actualizar el estado de la cita en la base de datos
        conexion = mysql.connection
        cursor = conexion.cursor()
        cursor.execute("UPDATE citas SET estado = %s WHERE id_cita = %s", (nuevo_estado, cita_id))
        conexion.commit()
        cursor.close()
        # Redirigir de vuelta a la página de administración de citas
        return redirect("/admin/citas")
"""
PAGOS CITAS
"""
@app.route('/admin/registrar_pago', methods=['GET'])
def mostrar_formulario_pago():
    return render_template('admin/pago.html')
@app.route('/admin/realizar_pago', methods=['POST'])
def realizar_pago():
    if request.method == 'POST':
        try:
            dni_cliente = request.form['dni_cliente']
            monto = request.form['monto']
            fecha_pago = request.form['fecha_pago']
            corte_realizado = request.form['corte_realizado']
            # Consulta SQL para obtener el ID de la cita del cliente usando su DNI
            consulta_sql = """
                SELECT c.id_cita
                FROM citas c
                JOIN usuario u_cliente ON c.id_cliente = u_cliente.id_usuario
                WHERE u_cliente.numeroDeDocumento = %s
            """
            conexion = mysql.connection
            cursor = conexion.cursor()
            cursor.execute(consulta_sql, (dni_cliente,))
            id_cita = cursor.fetchone()[0]  # Obtener el ID de la cita
            cursor.close()
            # Insertar el pago en la base de datos
            consulta_insert = """
                INSERT INTO pagos (id_cita, monto, fechaPago, corteRealizado)
                VALUES (%s, %s, %s, %s)
            """
            cursor = conexion.cursor()
            cursor.execute(consulta_insert, (id_cita, monto, fecha_pago, corte_realizado))
            conexion.commit()
            cursor.close()
            return "Pago realizado correctamente."
        except Exception as e:
            return f"Error al realizar el pago: {str(e)}"
        finally:
            if conexion:
                # conexion.close()
                pass
@app.route('/logout')
def logout():
    session.clear()  # Limpiar todos los datos de la sesión
    return redirect(url_for('cliente_login'))  # Redirigir al usuario a la página de inicio de sesión

if __name__ == '__main__':
    app.run(debug=True)
