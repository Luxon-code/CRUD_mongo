from app import app,productos
from flask import request,render_template,redirect
import pymongo
@app.route('/')
def index():
    return render_template('listarProductos.html',listaProducto = listarProductos())
@app.route('/vistaAgregarProducto')
def vistaAgregarProducto():
    producto = {"categoria":""}
    return render_template('frmAgregar.html',producto = producto)
@app.route('/vistaActualizarProducto')
def vistaActualizarProducto():
    producto = {}
    return render_template('frmActualizar.html',producto = producto)
@app.route('/agregarProducto',methods=['POST'])
def agregarProductos():
    try:
        Codigo = int(request.form['txtCodigo'])
        nombre = request.form['txtNombre']
        precio = int(request.form['txtPrecio'])
        categoria = request.form['cbCategoria']
        producto = {
            "codigo": Codigo,
            "nombre": nombre,
            "precio": precio,
            "categoria": categoria
        }
        if existeProducto(Codigo):
            mensaje = "Ya existe un producto con este codigo"
            return render_template('frmAgregar.html',producto=producto,mensaje = mensaje)
        else:
            resultado = productos.insert_one(producto)
            mensaje ="Producto agregado Correctamente"
            return redirect('/')
    except pymongo.errors as  error:
        mensaje= error
        return render_template('frmAgregar.html',producto=producto,mensaje = mensaje)
@app.route('/consultar/<int:codigo>', methods=['GET'])        
def consultarPorCodigo(codigo):
    try:
        consulta = {"codigo": codigo}
        producto = productos.find_one(consulta)
        if producto is not None:
            return redirect("/vistaActualizarProducto") and render_template("frmActualizar.html", producto= producto)
    except pymongo.errors as error:
        mensaje = error
    return render_template("listarProductos.html",mensaje=mensaje)
def existeProducto(codigoConsulta):
    try:
        consulta = {"codigo": codigoConsulta}
        producto = productos.find_one(consulta)
        if producto is not None:
            return True
        else:
           return False
    except pymongo.errors as error:
        print(error)
@app.route("/actualizarProducto/<int:codigoA>",methods=["POST"])
def actualizarProducto(codigoA):
    try:
        codigoProducto = codigoA 
        codigo = int(request.form['txtCodigo'])
        nombre = request.form['txtNombre']
        precio = int(request.form['txtPrecio'])
        categoria = request.form['cbCategoria']
        criterio = {"codigo": codigoProducto}
        if existeProducto(codigoProducto):
            datosActualizar = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": categoria
            }
            consulta = {"$set": datosActualizar}
            resultado = productos.update_one(criterio,consulta)
            mensaje = "Producto Actualizado"
            return redirect('/') and render_template("listarProductos.html",mensaje=mensaje,listaProducto = listarProductos())
    except pymongo.errors as error:
        mensaje = error
    return render_template("frmActualizar.html",mensaje=mensaje)
@app.route("/eliminar/<int:codigo>", methods=["GET"])
def eliminarProducto(codigo):
    try:
        consulta = {"codigo": codigo}
        productos.delete_one(consulta)
        if existeProducto(codigo):
            mensaje="No se ha podido eliminar el producto"
        else:
            mensaje="Producto eliminado Correctamente"
    except pymongo.errors as error:
        mensaje= error
    return render_template("listarProductos.html",listaProducto = listarProductos(),mensaje=mensaje)
def listarProductos():
    try:
        listaProductos = productos.find()
        return listaProductos
    except pymongo.errors as error:
        return error