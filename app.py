from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'almacen'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    productos = cur.fetchall()
    cur.close()
    return render_template('index.html', productos=productos)

@app.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':

        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad = request.form['cantidad']


        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO productos (nombre, descripcion, precio, cantidad) VALUES (%s, %s, %s, %s)', (nombre, descripcion, precio, cantidad))
            mysql.connection.commit()
            cur.close()

            flash(f'Producto "{nombre}" agregado satisfactoriamente', 'success')

            return redirect(url_for('mensaje', category='success', message=f'Producto {nombre} agregado satisfactoriamente'))

        except Exception as e:
            flash(f'Error al agregar producto: {str(e)}', 'danger')

    return render_template('crear_producto.html')

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE id = %s', (id,))
    producto = cur.fetchone()
    cur.close()

    if producto is None:
        flash('Producto no encontrado', 'warning')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad = request.form['cantidad']

        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, cantidad = %s WHERE id = %s', (nombre, descripcion, precio, cantidad, id))
            mysql.connection.commit()
            cur.close()

            flash('Producto actualizado satisfactoriamente', 'success')

            return redirect(url_for('mensaje', category='success', message=f'Producto {nombre} actualizado satisfactoriamente'))

        except Exception as e:
            flash(f'Error al actualizar producto: {str(e)}', 'danger')

    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM productos WHERE id = %s', (id,))
        mysql.connection.commit()
        cur.close()

        flash('Producto eliminado satisfactoriamente', 'success')

    except Exception as e:
        flash(f'Error al eliminar producto: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.route('/mensaje/<category>/<message>')
def mensaje(category, message):
    return render_template('mensaje.html', category=category, message=message)

if __name__ == '__main__':
    app.run(debug=True)
