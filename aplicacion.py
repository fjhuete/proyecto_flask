from flask import Flask, render_template, abort, redirect, request
import json
app = Flask(__name__)

with open("static/data/eurovision.json") as f:
    datos=json.load(f)

@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/buscador')
def buscador():
    return render_template("buscador.html")

@app.route('/lista', methods=["POST"])
def lista():
    ciudad = request.form.get("ciudad")
    lista = []
    for i in datos:
        if i["city"] == ciudad:
            print(i["city"])
            elemento = {}
            elemento["year"] = i["year"]
            elemento["recinto"] = i["arena"]
            elemento["participantes"] = len(i["contestants"])
            lista.append(elemento)
    return render_template("resultado.html",ciudad=ciudad, lista=lista)

app.run("0.0.0.0",5000,debug=True)

