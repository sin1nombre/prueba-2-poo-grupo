from abc import ABC, abstractmethod
import datetime as dt
import re

# clase validador de entradas
class ValidadorEntrada:
    @staticmethod
    def sanitizar_texto(input_str: str) -> str:
        return input_str.strip()

    @staticmethod
    def validar_email(email: str) -> bool:
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(patron, email))

    @staticmethod
    def validar_horas(horas: float) -> bool:
        return 0.0 < horas <= 24.0
    
#clases de usuario y administrador
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

# clase servicio de autenticación
class ServicioAutenticacion:
    def __init__(self):
        self.__usuarios_registrados: list[Usuario] = []

    def registrar_usuario(self, usuario: Usuario) -> None:
        self.__usuarios_registrados.append(usuario)

    def login(self, username: str, pass_: str) -> bool:
        for usuario in self.__usuarios_registrados:
            if usuario.obtener_nombre_usuario() == username:
                return usuario.autenticar(pass_)
        return False

    def verificar_permiso(self, usuario: Usuario, modulo: str) -> bool:
        # Los administradores tienen acceso a todos los módulos
        if usuario.obtener_rol().lower() == "admin":
            return True
        return False

#clase registro de tiempo
class RegistroTiempo:
    def __init__(self, id_registro: str, fecha: dt.date, horas_trabajadas: float, descripcion_tareas: str, proyecto: "Proyecto"):
        self.__id_registro = id_registro
        self.__fecha = fecha
        self.__horas_trabajadas = horas_trabajadas
        self.__descripcion_tareas = descripcion_tareas
        self.__proyecto = proyecto

    def obtener_id_registro(self) -> str:
        return self.__id_registro

    def obtener_fecha(self) -> dt.date:
        return self.__fecha

    def obtener_horas_trabajadas(self) -> float:
        return self.__horas_trabajadas

    def obtener_descripcion_tareas(self) -> str:
        return self.__descripcion_tareas

    def obtener_proyecto(self) -> "Proyecto":
        return self.__proyecto

    def validar_horas(self) -> bool:
        return ValidadorEntrada.validar_horas(self.__horas_trabajadas)

    def __str__(self) -> str:
        return f"Registro {self.__id_registro} [{self.__fecha}]: {self.__horas_trabajadas} hrs - {self.__descripcion_tareas}"
    
# clase proyecto
class Proyecto:
    def __init__(self, id_proyecto: str, nombre: str, descripcion: str, fecha_inicio: dt.date):
        self.__id_proyecto = id_proyecto
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio
        self.__empleados_asignados: list["Empleado"] = []
        self.__registros_tiempo: list[RegistroTiempo] = []

    def obtener_id_proyecto(self) -> str:
        return self.__id_proyecto

    def obtener_nombre(self) -> str:
        return self.__nombre

    def obtener_descripcion(self) -> str:
        return self.__descripcion

    def obtener_fecha_inicio(self) -> dt.date:
        return self.__fecha_inicio

    def asignar_empleado(self, emp: "Empleado") -> None:
        if emp not in self.__empleados_asignados:
            self.__empleados_asignados.append(emp)

    def desasignar_empleado(self, emp: "Empleado") -> None:
        if emp in self.__empleados_asignados:
            self.__empleados_asignados.remove(emp)

    def agregar_registro_tiempo(self, registro: RegistroTiempo) -> None:
        self.__registros_tiempo.append(registro)

    def obtener_registros_tiempo(self) -> list[RegistroTiempo]:
        return self.__registros_tiempo

    def __str__(self) -> str:
        return f"Proyecto: {self.__nombre} (Inicio: {self.__fecha_inicio})"

# clase empleado
class Empleado:
    def __init__(self, nombre: str, id_empleado: str, direccion: str, telefono: str, email: str, fecha_inicio_contrato: dt.date, salario: float, usuario: Usuario = None):
        self.__nombre = nombre
        self.__id_empleado = id_empleado
        self.__direccion = direccion
        self.__telefono = telefono
        self.__email = email
        self.__fecha_inicio_contrato = fecha_inicio_contrato
        self.__salario = salario
        self.__usuario = usuario
        self.__registros: list[RegistroTiempo] = []

    def obtener_id_empleado(self) -> str:
        return self.__id_empleado

    def obtener_nombre(self) -> str:
        return self.__nombre

    def registrar_horas(self, proyecto: Proyecto, fecha: dt.date, horas: float, desc: str, id_registro: str) -> RegistroTiempo:
        nuevo_registro = RegistroTiempo(id_registro, fecha, horas, desc, proyecto)
        if nuevo_registro.validar_horas():
            self.__registros.append(nuevo_registro)
            proyecto.agregar_registro_tiempo(nuevo_registro)
            return nuevo_registro
        raise ValueError("Cantidad de horas inválida.")

    def obtener_datos_personales(self) -> str:
        return (f"ID: {self.__id_empleado} | Nombre: {self.__nombre} | "
                f"Email: {self.__email} | Teléfono: {self.__telefono} | "
                f"Dirección: {self.__direccion} | Salario: ${self.__salario}")

    def __str__(self) -> str:
        return f"{self.__nombre} (ID: {self.__id_empleado})"
    
# clase departamento
class Departamento:
    def __init__(self, id_departamento: str, nombre: str):
        self.__id_departamento = id_departamento
        self.__nombre = nombre
        self.__gerente: Empleado | None = None
        self.__empleados: list[Empleado] = []

    def obtener_id(self) -> str:
        return self.__id_departamento

    def obtener_nombre(self) -> str:
        return self.__nombre

    def agregar_empleado(self, emp: Empleado) -> None:
        if emp not in self.__empleados:
            self.__empleados.append(emp)

    def remover_empleado(self, emp: Empleado) -> None:
        if emp in self.__empleados:
            self.__empleados.remove(emp)
        if self.__gerente == emp:
            self.__gerente = None

    def asignar_gerente(self, gerente: Empleado) -> None:
        self.__gerente = gerente
        self.agregar_empleado(gerente)

    def remover_gerente(self, gerente: Empleado) -> None:
        if self.__gerente == gerente:
            self.__gerente = None

    def listar_empleados(self) -> list[Empleado]:
        return self.__empleados

    def __str__(self) -> str:
        nom_gerente = self.__gerente.obtener_nombre() if self.__gerente else "Sin gerente"
        return f"Depto: {self.__nombre} | Gerente: {nom_gerente} | Cant. Empleados: {len(self.__empleados)}"

# clase informe abstracta
class Informe(ABC):
    def __init__(self, id_informe: str, fecha_generacion: dt.date, titulo: str):
        self._id_informe = id_informe
        self._fecha_generacion = fecha_generacion
        self._titulo = titulo

    @abstractmethod
    def generar_informe(self) -> None:
        pass

    @abstractmethod
    def exportar(self) -> None:
        pass

    def __str__(self) -> str:
        return f"Informe: {self._titulo} ({self._fecha_generacion})"

# clase informe PDF
class InformePDF(Informe):
    def __init__(self, id_informe: str, fecha_generacion: dt.date, titulo: str, plantilla_estilo: str):
        super().__init__(id_informe, fecha_generacion, titulo)
        self.__plantilla_estilo = plantilla_estilo

    def generar_informe(self) -> None:
        print(f"Generando informe PDF '{self._titulo}' usando plantilla: {self.__plantilla_estilo}...")

    def exportar(self) -> None:
        print(f"Exportando {self._titulo}.pdf exitosamente.")

# clase informe Excel
class InformeExcel(Informe):
    def __init__(self, id_informe: str, fecha_generacion: dt.date, titulo: str, nombre_hoja: str):
        super().__init__(id_informe, fecha_generacion, titulo)
        self.__nombre_hoja = nombre_hoja

    def generar_informe(self) -> None:
        print(f"Generando hoja Excel '{self._titulo}' en la hoja: {self.__nombre_hoja}...")

    def exportar(self) -> None:
        print(f"Exportando {self._titulo}.xlsx exitosamente.")
