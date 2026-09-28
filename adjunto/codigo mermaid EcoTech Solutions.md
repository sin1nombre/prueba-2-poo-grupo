```
classDiagram
	class Usuario {
		- id_usuario : Str
		- nombre_usuario : Str
		- contraseña : Str
		- rol : Str
		+ autenticar(contraseña) Boolean
		+ cambiar_contrasena(nueva) Boolean
	}
	
	class Empleado {
		- id_empleado : Str
		- nombre : Str
		- direccion : Str
		- telefono : Str
		- email : Str
		- fecha_inicio_contrato : Date
		- salario : Double
		+ registrar_horas(proyecto, fecha, horas, desc) RegistroTiempo
		+ obtener_datos_personales() Str
	}
	
	class Administrador {
		+ crear_departamento(nombre) Departamento
		+ asignar_empleado_departamento(emp, depto) none
		+ crear_proyecto(nombre, desc, fecha) Proyecto
		+ solicitar_informe(tipo, formato) Informe
	}
	
	class Departamento {
		- id_departamento : Str
		- nombre : Str
		+ agregar_empleado(emp) none
		+ remover_empleado(emp) none
		+ asignar_gerente(gerente) none
		+ remover_gerente(gerente) none
		+ listar_empleados() List~Empleado~
	}
	
	class Proyecto {
		- id_proyecto : Str
		- nombre : Str
		- descripcion : Str
		- fecha_inicio : Date
		+ asignar_empleado(emp) none
		+ desasignar_empleado(emp) none
		+ obtener_registros_tiempo() List~RegistroTiempo~
	}
	
	class RegistroTiempo {
		- Str id_registro : Str
		- fecha : Date
		- horas_trabajadas : Double
		- descripcion_tareas : Str
		+ validar_horas() Boolean
	}
	
	class Informe {
		- id_informe : Str
		- fecha_generacion : Date
		- titulo : Str
		+ generar_informe() none
		+ exportar() none
	}
	
	class InformePDF {
	}
	
	class InformeExcel {
	}
	
	class ServicioAutenticacion {
		+ login(username, pass) Boolean
		+ verificar_permiso(usuario, modulo) Boolean
	}
	
	class ServicioCifrado {
		+ cifrar_datos(datos) Str
		+ descifrar_datos(datos_cifrados) Str
		+ contraseña_hash(pass) Str
	}
	
	class ValidadorEntrada {
		+ sanitizar_Texto(input) Str
		+ validar_email(email) Boolean
		+ validar_horas(horas) Boolean
	}

	%% Herencia
	Usuario <|-- Empleado
	Empleado <|-- Administrador
	Informe <|-- InformePDF
	Informe <|-- InformeExcel

	%% Agregación
	Departamento "1" o-- "0..*" Empleado

	%% Asociación dirigida
	Departamento "0..1" --> "1" Empleado

	%% Asociación simple
	Empleado "1..*" -- "0..*" Proyecto
	Proyecto "1" -- "0..*" RegistroTiempo

	%% Composición
	Empleado "1" *-- "0..*" RegistroTiempo

	%% Dependencia
	ServicioAutenticacion ..> Usuario
	ServicioCifrado ..> Empleado
	Administrador ..> Informe
	RegistroTiempo ..> ValidadorEntrada
```
