from flask import Flask,request,render_template
import pymongo
app = Flask(__name__)
#Crear conexiona mongo
miConexion = pymongo.MongoClient("mongodb://localhost:27017")
#acceder a la base de datos
basedatos = miConexion["GestionProductos"]
#crear obejeto para referenciar a la coleccion
productos = basedatos["Productos"]
from controller.controllerProducto import *
if __name__ == "__main__":
    app.run(port=3000,debug=True)