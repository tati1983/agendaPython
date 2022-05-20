# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 22:06:31 2022

@author:
        Francisco Peralta,
        Matias Ott,
        Violeta Dorati,
        Adrian Orellano
"""

from peewee import Model, SqliteDatabase, TextField, IntegerField
from peewee import DatabaseError
from observador import Observable

db = SqliteDatabase('tareas.db')


class BaseModel(Model):
    class Meta:
        database = db


class Tarea(BaseModel):
    titulo = TextField()
    fecha_hora_desde = IntegerField()
    fecha_hora_hasta = IntegerField()
    nota = TextField()
    contacto = TextField()
    tipo = TextField()
    recordar_cada_tipo = TextField()
    recordar_cada_cantidad = IntegerField()


class Modelo(Observable):
    def __init__(self, controlador):
        self.dentro_de_decorador_conectar = True
        self.controlador = controlador
        try:
            db.connect()
            db.create_tables([Tarea])
            db.close()
        except DatabaseError as error:
            self.controlador.mostrar_excepcion(
                "Error al crear DB - " + str(error))

    def decorador_imprimir_nombre_metodo(funcion):
        def envoltura(self, *args):
            print("# FUNCION : " + str(funcion.__name__))
            return funcion(self, *args)
        return envoltura

    def decorador_conectar_y_desconectar(funcion):
        def envoltura(*args):
            tabla = 0
            print("# Entra al decorador")
            if args[0].dentro_de_decorador_conectar:
                try:
                    db.connect()
                    print("# Conecta db")
                    args[0].dentro_de_decorador_conectar = False
                except DatabaseError as error:
                    args[0].controlador.mostrar_excepcion(
                        "Error al conectar a DB - " + str(error))

            tabla = funcion(*args)

            if not args[0].dentro_de_decorador_conectar:
                try:
                    print("# Desconecta db")
                    db.close()
                    args[0].dentro_de_decorador_conectar = True
                except DatabaseError as error:
                    args[0].controlador.mostrar_excepcion(
                        "Error al desconectar a DB - " + str(error))

            print("# Sale de decorador")
            print("")
            return tabla

        return envoltura

    @decorador_conectar_y_desconectar
    @decorador_imprimir_nombre_metodo
    def alta(self, parametros):
        try:
            tarea = Tarea()
            tarea.titulo = str(parametros[0])
            tarea.fecha_hora_desde = int(parametros[1])
            tarea.fecha_hora_hasta = int(parametros[2])
            tarea.nota = str(parametros[3])
            tarea.contacto = str(parametros[4])
            tarea.tipo = str(parametros[5])
            tarea.recordar_cada_tipo = str(parametros[6])
            tarea.recordar_cada_cantidad = int(parametros[7])
            tarea.save()

            parametros = ['', 10800, 4765143600, '', '', '', '', '']
            tareas = self.get_tareas(parametros)
            self.notificar_a_observador(tareas)  # Notifica al Observador

        except DatabaseError as error:
            self.controlador.mostrar_excepcion(
                "Error en alta a DB - " + str(error))

    @decorador_conectar_y_desconectar
    @decorador_imprimir_nombre_metodo
    def baja(self, id_a_eliminar):
        try:
            tarea = Tarea.get(Tarea.id == id_a_eliminar)
            tarea.delete_instance()
        except DatabaseError as error:
            self.controlador.mostrar_excepcion(
                "Error en baja a DB - " + str(error))

    @decorador_conectar_y_desconectar
    @decorador_imprimir_nombre_metodo
    def modificacion(self, parametros, id):
        try:
            tarea = Tarea.update(
                        titulo=str(parametros[0]),
                        fecha_hora_desde=int(parametros[1]),
                        fecha_hora_hasta=int(parametros[2]),
                        nota=str(parametros[3]),
                        contacto=str(parametros[4]),
                        tipo=str(parametros[5]),
                        recordar_cada_tipo=str(parametros[6]),
                        recordar_cada_cantidad=int(parametros[7])
                        ).where(Tarea.id == id)
            tarea.execute()
        except DatabaseError as error:
            self.controlador.mostrar_excepcion(
                "Error en modificacion a DB - " + str(error))

    @decorador_conectar_y_desconectar
    @decorador_imprimir_nombre_metodo
    def get_tareas(self, parametros):
        try:
            tareas = Tarea.select().where(
                Tarea.titulo.contains(str(parametros[0])),
                Tarea.fecha_hora_desde >= int(parametros[1]),
                Tarea.fecha_hora_hasta <= int(parametros[2]),
                Tarea.nota.contains(str(parametros[3])),
                Tarea.contacto.contains(str(parametros[4])),
                Tarea.tipo.contains(str(parametros[5])),
                Tarea.recordar_cada_tipo.contains(str(parametros[6])),
                Tarea.recordar_cada_cantidad.contains(str(parametros[7])))
            tabla_lista = []
            for tarea in tareas:
                tarea_tupla = []
                tarea_tupla.append(tarea.id)
                tarea_tupla.append(tarea.titulo)
                tarea_tupla.append(tarea.fecha_hora_desde)
                tarea_tupla.append(tarea.fecha_hora_hasta)
                tarea_tupla.append(tarea.nota)
                tarea_tupla.append(tarea.contacto)
                tarea_tupla.append(tarea.tipo)
                tarea_tupla.append(tarea.recordar_cada_tipo)
                tarea_tupla.append(tarea.recordar_cada_cantidad)
                tabla_lista.append(tuple(tarea_tupla))
            tabla = tuple(tabla_lista)
            return tabla
        except DatabaseError as error:
            self.controlador.mostrar_excepcion(
                "Error en select DB - " + str(error))
