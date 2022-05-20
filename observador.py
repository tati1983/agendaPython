# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 22:06:31 2022

@author:
        Francisco Peralta,
        Matias Ott,
        Violeta Dorati,
        Adrian Orellano
"""


class Observable:
    observadores = []

    def agregar_obj_observador(self, obj):
        self.observadores.append(obj)

    def quitar_obj_observador(self, obj):
        self.remove(obj)

    def notificar_a_observador(self, *args):
        for observador in self.observadores:
            observador.actualizar_observador(*args)


class Observador:

    def actualizar_observador(self):
        raise NotImplementedError("Delegación de actualización")
