from abc import ABC, abstractmethod
import datetime as dt
import re

class Usuario:
    def __init__(self, id_usuario: str, nombre_usuario: str, contrasena: str, rol: str):
        self.__id_usuario = id_usuario
        self.__nombre_usuario = nombre_usuario
        self.__contrasena = contrasena
        self.__rol = rol

    def obtener_id_usuario(self) -> str:
        return self.__id_usuario

    def obtener_nombre_usuario(self) -> str:
        return self.__nombre_usuario

    def obtener_rol(self) -> str:
        return self.__rol

    def autenticar(self, contrasena: str) -> bool:
        return self.__contrasena == contrasena

    def cambiar_contrasena(self, nueva: str) -> bool:
        if nueva and len(nueva) >= 4:
            self.__contrasena = nueva
            return True
        return False

    def __str__(self) -> str:
        return f"{self.__nombre_usuario} (Rol: {self.__rol})"
    
class Administrador(Usuario):
    def __init__(self, id_usuario: str, nombre_usuario: str, contrasena: str, rol: str = "Admin"):
        super().__init__(id_usuario, nombre_usuario, contrasena, rol)

    def crear_departamento(self, id_dept: str, nombre: str) -> "Departamento":
        return Departamento(id_dept, nombre)

    def asignar_empleado_departamento(self, emp: "Empleado", depto: "Departamento") -> None:
        depto.agregar_empleado(emp)

    def crear_proyecto(self, id_proyecto: str, nombre: str, desc: str, fecha: dt.date) -> "Proyecto":
        return Proyecto(id_proyecto, nombre, desc, fecha)

    def solicitar_informe(self, id_informe: str, titulo: str, tipo: str, formato: str) -> "Informe":
        if formato.lower() == "pdf":
            return InformePDF(id_informe, dt.date.today(), titulo, plantilla_estilo="Estandar")
        elif formato.lower() == "excel":
            return InformeExcel(id_informe, dt.date.today(), titulo, nombre_hoja="Datos")
        raise ValueError(f"Formato no soportado: {formato}")
    
