from abc import ABC, abstractmethod
import datetime as dt

class usuario(ABC):
    def __init__(self,id_usuario, nombre, email, contraseña,rol):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._email = email
        self._contraseña = contraseña
        self._rol = rol

    @abstractmethod
    def servicio_autenticacion(self, email, contraseña):
        pass