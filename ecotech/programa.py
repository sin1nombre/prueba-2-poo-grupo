from modelo import Medico, Paciente, Especialidad, Consultorio, Cita
import datetime as dt

especialidades = [
    Especialidad(1, "Cardiología", "Cardiología adultos"),
    Especialidad(2, "Neurología", "Neurología adultos"),
    Especialidad(3, "Pediatría", "Pediatría clinica"),
    ]

for especialidad in especialidades:
    print(especialidad)

consultorios = [
    Consultorio(1, "Box 01", "Edificio A, Piso 1"),
    Consultorio(2, "Box 02", "Edificio A, Piso 1"),
    Consultorio(3, "Pabellón Atlanta", "Edificio A, Piso 2"),
    Consultorio(4, "Sala Hospitalizados 1", "Edificio A, Piso 2"),
    ]

for consultorio in consultorios:
    print(consultorio)

medico = Medico("12345678-9", "Juan", "Perez", "123456789", "juan.perez@example.com", 1, "LIC-123456", 1000000)
print(medico)

medico.agregar_especialidad(especialidades[1])
medico.agregar_especialidad(especialidades[2])
print(f"Especialidades de {medico}")
for esp in medico.obtener_especialidades():
    print(f"{esp}")

paciente = Paciente("98765432-1", "Maria", "Gonzalez", "987654321", "maria.gonzalez@example.com", 1, "FIC-123456", dt.date(1990, 1, 1))
print(paciente)

cita = Cita(1, "Agendada", "Sintomas respiratorios", paciente, medico)
cita.modificar_consultorio(consultorios[0])
print(f"Datos de la cita {cita}")
print(f"Paciente: {cita.obtener_paciente()}")
print(f"Medico: {cita.obtener_medico()}")
print(f"Especialidades del médico")
for esp in cita.obtener_medico().obtener_especialidades():
    print(f"{esp}")
print(f"Consultorio: {cita.obtener_consultorio()}")

