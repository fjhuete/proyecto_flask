from flask import Flask, render_template, abort, redirect, request
import json
import os

app = Flask(__name__)
port = os.getenv("PORT")

with open("static/data/eurovision.json") as f:
    datos=json.load(f)
with open("static/data/countries.json") as g:
    paises=json.load(g)

@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/buscador', methods=["GET","POST"])
def buscador():
    years=[]
    for i in datos:
       years.append(i["year"])
    if request.method == "GET":
        return render_template("buscador.html", years=years)
    elif request.method == "POST":
        ciudad = request.form.get("ciudad")
        year = int(request.form.get("year"))
        lista = []
        if year == 0:
            for i in datos:
                if (i["city"])[:len(ciudad)] == ciudad:
                    elemento = {}
                    elemento["ciudad"] = i["city"]
                    elemento["year"] = i["year"]
                    elemento["recinto"] = i["arena"]
                    elemento["participantes"] = len(i["contestants"])
                    lista.append(elemento)
        else:
            for i in datos:
                if (i["city"])[:len(ciudad)] == ciudad and i["year"] == year:
                    elemento = {}
                    elemento["ciudad"] = i["city"]
                    elemento["year"] = i["year"]
                    elemento["recinto"] = i["arena"]
                    elemento["participantes"] = len(i["contestants"])
                    lista.append(elemento)
                
        return render_template("resultado.html",ciudad=ciudad, lista=lista, years=years, seleccionado=int(year))

@app.route('/lista', methods=["POST"])
def lista():
    ciudad = request.form.get("ciudad")
    lista = []
    for i in datos:
        if (i["city"])[:len(ciudad)] == ciudad:
            elemento = {}
            elemento["ciudad"] = i["city"]
            elemento["year"] = i["year"]
            elemento["recinto"] = i["arena"]
            elemento["participantes"] = len(i["contestants"])
            lista.append(elemento)
    return render_template("resultado.html",ciudad=ciudad, lista=lista)

@app.route('/detalle')
def detalles():
    year=int(request.args.get("year"))
    for i in datos:
        if i["year"] == year:
            elemento = {}
            elemento["ciudad"] = i["city"]
            elemento["year"] = i["year"]
            elemento["recinto"] = i["arena"]
            elemento["participantes"] = len(i["contestants"])
            if i.get("logoUrl"):
                elemento["img"] = i["logoUrl"]
            participantes = []
            for participante in i["contestants"]:
                concursante = {}
                concursante["nombre"] = participante["artist"]
                concursante["cancion"] = participante["song"]
                concursante["pais"] = paises[(participante["country"])]
                if i.get("logoUrl"):
                    concursante["video"] = participante["videoUrls"][0]
                participantes.append(concursante)
            elemento["lista"] = participantes
            return render_template("detalle.html",year=year, elemento=elemento)
    return abort(404)

@app.route('/concursante')
def concursante():
    year=int(request.args.get("year"))
    nombre=str(request.args.get("nombre"))
    for i in datos:
        if i["year"] == year:
            for participante in i["contestants"]:
                if participante["artist"] == nombre:
                    concursante = {}
                    concursante["id"] = participante["id"]
                    concursante["nombre"] = participante["artist"]
                    concursante["cancion"] = participante["song"]
                    concursante["pais"] = paises[(participante["country"])]
                    if participante.get("videoUrls"):
                        concursante["video"] = participante["videoUrls"][0]
                    if participante.get("composers"):
                        concursante["compositores"] = participante["composers"]
                    if participante.get("lyricists"):
                        concursante["letristas"] = participante["lyricists"]
            tabla={}
            for ronda in i["rounds"]:
                for j in ronda["performances"]:
                    if j["contestantId"] == concursante["id"]:
                        puntos = j["scores"]
                        for votos in puntos:
                            if votos["name"] == "total":
                                resultado={}
                                for elemento in votos["votes"].items():
                                    pais = paises[elemento[0]]
                                    resultado[pais] = elemento[1]
                                total=votos["points"]
                                resultado["Total"]=total
                        tabla[ronda["name"]]=resultado

    return render_template("puntuaciones.html",year=year, nombre=nombre, concursante=concursante, tabla=tabla, resultado=resultado)
    #return abort(404)
    

app.run("0.0.0.0",port,debug=True)

