#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 2.0

Descripcion:
Programa creado para administrar la base de datos de registro de personas
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from numpy import append
db = SQLAlchemy()

class Persona(db.Model):
    __tablename__ = "persona"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Persona:{self.name} de edad {self.age}"


def insert(name, age):
    # Crear una nueva persona
    person = Persona(name=name, age=age)

    # Agregar la persona a la DB
    db.session.add(person)
    db.session.commit()


def report(limit=0, offset=0):
    # Obtener todas las personas
    query = db.session.query(Persona)
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    json_result_list = []

    # De los resultados obtenidos pasar a un diccionario
    # que luego será enviado como JSON
    # TIP --> la clase Persona podría tener una función
    # para pasar a JSON/diccionario
    for person in query:
        json_result = {'name': person.name, 'age': person.age}
        json_result_list.append(json_result)

    return json_result_list

def dashboard():
    # Obtener los últimos 250 registros del paciente
    # ordenado por fecha, obteniedo los últimos 250 registros
    query = db.session.query(Persona).order_by(Persona.name.desc())
    #query = query.limit(250)
    query_results = query.all()

    if query_results is None or len(query_results) == 0:
        # No data register
        # Bug a proposito dejado para poner a prueba el traceback
        # ya que el sistema espera una tupla
        return []

    x = []
    y = []

    # De los resultados obtenidos tomamos el tiempo y las puslaciones pero
    # en el orden inverso, para tener del más viejo a la más nuevo registro
    for resultados in query_results:
        x.append(resultados.name)
        y.append(resultados.age)

    return x, y

if __name__ == "__main__":
    print("Test del modulo heart.py")

    # Crear una aplicación Flask para testing
    # y una base de datos fantasma (auxiliar o dummy)
    # Referencia:
    # https://stackoverflow.com/questions/17791571/how-can-i-test-a-flask-application-which-uses-sqlalchemy
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdatabase.db"
    # Bindear la DB con nuestra app Flask
    db.init_app(app)
    app.app_context().push()

    db.create_all()

    # Aquí se puede ensayar todo lo que necesitemos con nuestra DB
    # ...

    db.session.remove()
    db.drop_all()