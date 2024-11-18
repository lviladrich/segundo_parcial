import json
from datetime import datetime, timedelta

# Función para imprimir separadores con colores
def imprimir_separador(mensaje=""):
    print("\n" + "=" * 50)
    if mensaje:
        print(f"✨ {mensaje} ✨")
    print("=" * 50)

# Función para cargar los usuarios desde el archivo
def cargar_usuarios(archivo):
    try:
        with open(archivo, 'r') as f:
            usuarios = json.load(f)
            # Asegúrate de que las claves (DNI) sean enteros
            usuarios = {int(k): v for k, v in usuarios.items()}
            return usuarios
    except (FileNotFoundError, json.JSONDecodeError):
        print("El archivo de usuarios no existe o está dañado. Creando archivo con usuarios predeterminados.")
        usuarios = {
            45622304: "Renzo",
            4: "M"
        }
        guardar_usuarios(archivo, usuarios)
        return usuarios

# Función para guardar usuarios en el archivo JSON
def guardar_usuarios(archivo, usuarios):
    with open(archivo, 'w') as f:
        json.dump(usuarios, f, indent=4)

# Función de autenticación de usuario
def autenticar_usuario(archivo_usuarios):
    usuarios = cargar_usuarios(archivo_usuarios)
    intentos = 0
    while intentos < 3:
        imprimir_separador("🔑 Ingreso al Sistema 🔑")
        try:
            dni_usuario = int(input("Ingresa tu DNI: "))
        except ValueError:
            print("⚠ El DNI debe ser un número entero. Intenta de nuevo.")
            intentos += 1
            continue
        
        nombre_usuario = input("Ingresa tu nombre: ")

        # Verificamos si el DNI está en los usuarios cargados
        if dni_usuario in usuarios:
            # Comprobamos si el nombre asociado al DNI es correcto
            if usuarios[dni_usuario] == nombre_usuario:
                print("✅ Bienvenido.")
                return dni_usuario
            else:
                print(f"❌ El nombre '{nombre_usuario}' no corresponde al DNI {dni_usuario}.")
        else:
            print(f"❌ El DNI {dni_usuario} no está registrado.")
        
        intentos += 1
        print(f"Te quedan {3 - intentos} intentos.")
    
    print("❌ Has fallado 3 veces. El acceso está bloqueado.")
    return None

# Función para cargar clientes desde un archivo JSON
def cargar_clientes(archivo):
    try:
        with open(archivo, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Función para guardar clientes en un archivo JSON
def guardar_clientes(archivo, clientes):
    with open(archivo, 'w') as f:
        json.dump(clientes, f, indent=4)

# Función para solicitar DNI
def solicitar_dni():
    while True:
        try:
            dni = int(input("Por favor, ingrese el DNI: "))
            if 5 < len(str(dni)) < 15:
                return dni
            else:
                print("⚠ El DNI debe tener entre 6 y 14 dígitos. Intente de nuevo.")
        except ValueError:
            print("❌ Entrada inválida. Asegúrese de ingresar solo números.")

# Función para solicitar una fecha
def solicitar_fecha(mensaje):
    while True:
        imprimir_separador()
        fecha_str = input(f"{mensaje} (YYYY-MM-DD): ")
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha
        except ValueError:
            print("⚠ Formato de fecha inválido. Usa 'YYYY-MM-DD'.")

# Función para generar el calendario de habitaciones
def generar_calendario_por_habitaciones(inicio, fin, habitaciones):
    calendario = {}
    for habitacion in habitaciones:
        calendario[habitacion] = [(inicio + timedelta(days=i), "disponible") for i in range((fin - inicio).days + 1)]
    return calendario

# Función para mostrar el calendario de una habitación
def mostrar_calendario(habitacion, calendario):
    imprimir_separador(f"📅 Calendario de la Habitación {habitacion} 📅")
    for fecha, estado in calendario[habitacion]:
        print(f"{fecha.strftime('%Y-%m-%d')}: {'Disponible' if estado == 'disponible' else 'Reservado'}")
    imprimir_separador()

# Función para realizar una reserva
def realizar_reserva(calendario, archivo_clientes):
    imprimir_separador("🏨 Realizar Reserva 🏨")
    habitaciones_disponibles = [hab for hab, fechas in calendario.items() if any(est == "disponible" for _, est in fechas)]

    if not habitaciones_disponibles:
        print("❌ No hay habitaciones disponibles.")
        return

    print("Habitaciones disponibles:")
    for hab in habitaciones_disponibles:
        print(f"  - {hab}")

    habitacion = input("Introduce el nombre de la habitación que deseas reservar: ")

    if habitacion not in habitaciones_disponibles:
        print(f"La habitación '{habitacion}' no está disponible.")
        return

    # Mostrar calendario de la habitación seleccionada
    mostrar_calendario(habitacion, calendario)

    # Cargar clientes desde el archivo
    clientes = cargar_clientes(archivo_clientes)

    # Solicitar DNI
    dni = solicitar_dni()

    # Verificar si el cliente ya tiene una reserva en esta habitación
    if dni in clientes and habitacion in clientes[dni]["reservas"]:
        print(f"❌ Ya tienes una reserva en la habitación '{habitacion}'.")
        return

    # Si el cliente no tiene reserva, solicitar su nombre y apellido
    if dni not in clientes:
        nombre = input("Introduce tu nombre: ")
        apellido = input("Introduce tu apellido: ")

        # Agregar cliente al archivo
        clientes[dni] = {
            "nombre": nombre,
            "apellido": apellido,
            "reservas": []
        }

    fecha_entrada = solicitar_fecha("Introduce la fecha de entrada")
    fecha_salida = solicitar_fecha("Introduce la fecha de salida")

    while fecha_entrada >= fecha_salida:
        print("⚠ La fecha de entrada debe ser anterior a la fecha de salida.")
        fecha_entrada = solicitar_fecha("Introduce la fecha de entrada")
        fecha_salida = solicitar_fecha("Introduce la fecha de salida")

    # Verificar que las fechas existan en el calendario
    fechas_a_reservar = []
    fechas_no_disponibles = []

    for fecha in (fecha_entrada + timedelta(days=n) for n in range((fecha_salida - fecha_entrada).days + 1)):
        fecha_encontrada = False
        for i in range(len(calendario[habitacion])):
            if calendario[habitacion][i][0].date() == fecha.date():
                if calendario[habitacion][i][1] == "disponible":
                    fechas_a_reservar.append(fecha)
                else:
                    fechas_no_disponibles.append(fecha)
                fecha_encontrada = True
                break
        if not fecha_encontrada:
            print(f"🚫 La fecha {fecha.strftime('%Y-%m-%d')} no existe en el calendario de la habitación '{habitacion}'.")
            return

    # Mostrar días disponibles y no disponibles
    if (len(fechas_a_reservar)) > 0:
        print("\nDías disponibles para la reserva:")
        for fecha in fechas_a_reservar:
            print(f"  - {fecha.strftime('%Y-%m-%d')}")

    if (len(fechas_no_disponibles)) > 0:        
        print("\nDías no disponibles:")
        for fecha in fechas_no_disponibles:
            print(f"  - {fecha.strftime('%Y-%m-%d')}")

    if not fechas_a_reservar:
        print("❌ No hay días disponibles en el rango seleccionado.")
        return

    # Confirmar la reserva
    while True:
        confirmar = input("¿Deseas confirmar la reserva? (s/n): ").lower()
        if confirmar == 's':
            # Marcar las fechas como reservadas
            for fecha in fechas_a_reservar:
                for i in range(len(calendario[habitacion])):
                    if calendario[habitacion][i][0].date() == fecha.date():
                        calendario[habitacion][i] = (calendario[habitacion][i][0], "reservado")

            # Guardar la reserva del cliente
            clientes[dni]["reservas"].append({
                "habitacion": habitacion,
                "fecha_entrada": fecha_entrada.strftime('%Y-%m-%d'),
                "fecha_salida": fecha_salida.strftime('%Y-%m-%d'),
                "dias": (fecha_salida - fecha_entrada).days,
                "fechas_reservadas": [fecha.strftime('%Y-%m-%d') for fecha in fechas_a_reservar]
            })

            # Guardar clientes en el archivo
            guardar_clientes(archivo_clientes, clientes)
            print("✅ Reserva confirmada.")
            break
        elif confirmar == 'n':
            print("❌ Reserva cancelada.")
            break

# Función para buscar reservas por DNI
def buscar_reserva(archivo_clientes):
    imprimir_separador("🔍 Buscar Reserva 🔍")
    dni = solicitar_dni()

    clientes = cargar_clientes(archivo_clientes)

    if dni in clientes:
        reservas = clientes[dni]["reservas"]
        if reservas:
            print(f"🎟 Reservas de {clientes[dni]['nombre']} {clientes[dni]['apellido']}:")
            for reserva in reservas:
                print(f"  - Habitacion: {reserva['habitacion']}, Entrada: {reserva['fecha_entrada']}, Salida: {reserva['fecha_salida']}, Dias: {reserva['dias']}")
        else:
            print("❌ No tienes reservas.")
    else:
        print("❌ No se encontró un cliente con ese DNI.")

# Función principal
def main():
    archivo_usuarios = "usuarios.json"
    archivo_clientes = "clientes.json"

    dni_usuario = autenticar_usuario(archivo_usuarios)

    if dni_usuario is None:
        return

    # Inicializar calendario y habitaciones
    habitaciones = ["A101", "A102", "B101", "B102"]
    inicio = datetime.today()
    fin = inicio + timedelta(days=30)  # 30 días hacia adelante
    calendario = generar_calendario_por_habitaciones(inicio, fin, habitaciones)
    
    while True:
        imprimir_separador("🌟 Menú de Opciones 🌟")
        print("1. Realizar reserva")
        print("2. Buscar reserva por DNI")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            realizar_reserva(calendario, archivo_clientes)
        elif opcion == "2":
            buscar_reserva(archivo_clientes)
        elif opcion == "3":
            print("👋 Hasta pronto!")
            break
        else:
            print("⚠ Opción inválida.")

# Ejecutar el programa

main()