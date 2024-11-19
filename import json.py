import json
from datetime import datetime, timedelta
import re
from functools import reduce


def imprimir_linea():
    print("==================================================")


# Función para imprimir separadores con colores
def imprimir_separador(mensaje=""):
    print("\n" + "=" * 50)
    if mensaje:
        print(f"✨ {mensaje} ✨")
    print("=" * 50)


# Función para cargar los usuarios desde el archivo
def cargar_usuarios(archivo):
    try:
        with open(archivo, "r") as f:
            data = json.load(f)
            dni_existentes = set()  # Conjunto para evitar duplicados
            usuarios = {}
            for dni, nombre in data.items():
                if int(dni) not in dni_existentes:
                    usuarios[int(dni)] = nombre
                    dni_existentes.add(int(dni))
                else:
                    print(f"⚠ El DNI {dni} está duplicado y será ignorado.")
            return usuarios
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = {45622304: "Renzo", 455125: "MIRANDA"}
        guardar_usuarios(archivo, usuarios)
        return usuarios


# Función para guardar usuarios en el archivo JSON
def guardar_usuarios(archivo, usuarios):
    with open(archivo, "w") as f:
        json.dump(usuarios, f, indent=4)


# Función de autenticación de usuario
def autenticar_usuario(archivo_usuarios):
    usuarios = cargar_usuarios(archivo_usuarios)
    intentos = 0
    imprimir_separador("🔑 Ingreso al Sistema 🔑")
    try:
        dni_usuario = int(input("Ingresa tu ID: "))
    except ValueError:
        print("⚠ El ID debe ser un número entero. Intenta de nuevo.")
        intentos += 1
    while dni_usuario not in usuarios and intentos <= 4:
        print(f"❌ El ID {dni_usuario} no está registrado.")
        intentos += 1
        print(f"Te quedan {5 - intentos} intentos.")
        if intentos <= 4:
            imprimir_linea()
            dni_usuario = int(input("Ingresa tu ID: "))

    if intentos <= 4:
        print(f"✅ ID {dni_usuario} encontrado en el sistema")
        imprimir_linea()
        nombre_usuario = input("Ingresa tu contraseña: ")

    while dni_usuario in usuarios and intentos <= 4:
        # Comprobamos si el nombre asociado al DNI es correcto
        if usuarios[dni_usuario] == nombre_usuario:
            imprimir_linea()
            print(f"✅ Bienvenido al Sistema {nombre_usuario}.")
            return dni_usuario
        else:
            print(
                f"❌ La contraseña '{nombre_usuario}' no corresponde al ID {dni_usuario}."
            )
            intentos += 1
            print(f"Te quedan {5 - intentos} intentos.")
            if intentos <= 4:
                imprimir_linea()
                nombre_usuario = input("Ingresa tu contraseña: ")
    if intentos >= 4:
        imprimir_linea()
        print("❌ Te quedaste sin intentos, bloqueando sistema por seguridad....")
        print("⚠ El acceso fue bloqueado.")
        return None


# Función para cargar clientes desde un archivo JSON
def cargar_clientes(archivo):
    try:
        with open(archivo, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Función para guardar clientes en un archivo JSON
def guardar_clientes(archivo, clientes):
    with open(archivo, "w") as f:
        json.dump(clientes, f, indent=4)


# Función para cargar clientes desde un archivo JSON
def cargar_clientes(archivo):
    try:
        with open(archivo, "r") as f:
            clientes = json.load(f)
            return clientes
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Función para guardar clientes en un archivo JSON
def guardar_clientes(archivo, nuevos_clientes):
    try:
        # Cargar clientes existentes
        clientes_existentes = cargar_clientes(archivo)

        for dni, datos_nuevos in nuevos_clientes.items():
            dni = str(dni)  # Asegurar que el DNI sea una cadena para consistencia
            if dni in clientes_existentes:
                # Cliente ya existe: combinar reservas
                reservas_existentes = clientes_existentes[dni].get("reservas", [])
                nuevas_reservas = datos_nuevos.get("reservas", [])

                # Agregar nuevas reservas sin duplicarlas
                for nueva_reserva in nuevas_reservas:
                    if nueva_reserva not in reservas_existentes:
                        reservas_existentes.append(nueva_reserva)

                # Actualizar el cliente con las reservas combinadas
                clientes_existentes[dni]["reservas"] = reservas_existentes
            else:
                # Cliente nuevo: agregar directamente
                clientes_existentes[dni] = datos_nuevos

        # Guardar los clientes actualizados en el archivo
        with open(archivo, "w") as f:
            json.dump(clientes_existentes, f, indent=4)

        print("✅ Clientes guardados correctamente.")
    except Exception as e:
        print(f"❌ Error al guardar clientes: {e}")


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
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("⚠ Formato de fecha inválido. Usa 'YYYY-MM-DD'.")


# Función para mostrar el calendario de una habitación
def mostrar_calendario_habitacion(calendario, habitaciones, inicio, fin):
    imprimir_separador("📅 Mostrar Calendario 📅")

    habitacion = input(
        f"Introduce el nombre de la habitación ({', '.join(habitaciones)}): "
    )
    if habitacion not in habitaciones:
        print(f"❌ La habitación '{habitacion}' no existe.")
        return

    try:
        anio = int(input("Introduce el año: "))

        # Obtener el rango de años con rebanado
        anio_inicio = inicio.year
        anio_fin = fin.year

        # Crear una lista de años dentro del rango de inicio y fin
        anos_disponibles = list(
            range(anio_inicio, anio_fin + 1)
        )  # +1 para incluir el año_fin

        # Verificar si el año ingresado está en el rango disponible
        if anio not in anos_disponibles:
            print(f"❌ El año debe estar entre {anio_inicio} y {anio_fin}.")
            return
    except ValueError:
        print("❌ Entrada inválida. Introduce un número entero para el año.")
        return

    imprimir_separador(f"📅 Calendario de {habitacion} para el año {anio} 📅")
    print("✔ Disponible | ❌ Ocupado\n")

    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    for mes in range(1, 13):
        imprimir_separador(f"{meses[mes - 1]} {anio}")
        fechas_del_mes = [
            (fecha, estado)
            for fecha, estado in calendario[habitacion]
            if fecha.year == anio and fecha.month == mes
        ]

        if fechas_del_mes:
            # Dividir las fechas en semanas para mejor visualización
            semanas = []
            semana = []

            for fecha, estado in fechas_del_mes:
                semana.append(
                    f"{fecha.strftime('%Y-%m-%d')} {'✔' if estado == 'disponible' else '❌'}"
                )
                if fecha.weekday() == 6:  # Si es domingo, es el final de la semana
                    semanas.append(semana)
                    semana = []

            # Agregar la última semana si no está vacía
            if semana:
                semanas.append(semana)

            # Mostrar las semanas
            for semana in semanas:
                print("  ".join(semana))
        else:
            print("No hay datos para este mes.")
    imprimir_separador()


# Función para realizar una reserva
def mostrar_habitaciones_disponibles(calendario):
    habitaciones_disponibles = [
        hab
        for hab, fechas in calendario.items()
        if any(est == "disponible" for _, est in fechas)
    ]
    if not habitaciones_disponibles:
        print("❌ No hay habitaciones disponibles.")
    else:
        print("Habitaciones disponibles:")
        for hab in habitaciones_disponibles:
            print(f"  - {hab}")
    return habitaciones_disponibles


# Función para verificar si el cliente tiene una reserva en la habitación
def verificar_reserva_existente(dni, habitacion, clientes):
    if dni in clientes and habitacion in clientes[dni]["reservas"]:
        print(f"❌ Ya tienes una reserva en la habitación '{habitacion}'.")
        return True
    return False


# Función para solicitar el DNI y verificar que el cliente esté registrado
def solicitar_dni_cliente(dni, clientes):
    if dni not in clientes:
        nombre = input("Introduce tu nombre: ").strip()
        apellido = input("Introduce tu apellido: ").strip()
        clientes[dni] = {"nombre": nombre, "apellido": apellido, "reservas": []}
    return clientes


# Función para validar las fechas de entrada y salida
def validar_fechas(fecha_entrada, fecha_salida):
    while fecha_entrada >= fecha_salida:
        print("⚠ La fecha de entrada debe ser anterior a la fecha de salida.")
        fecha_entrada = solicitar_fecha("Introduce la fecha de entrada")
        fecha_salida = solicitar_fecha("Introduce la fecha de salida")
    return fecha_entrada, fecha_salida


# Función para comprobar la disponibilidad de fechas en el calendario
def comprobar_disponibilidad_fechas(
    fecha_entrada, fecha_salida, habitacion, calendario
):
    fechas_a_reservar = []
    fechas_no_disponibles = []

    for fecha in (
        fecha_entrada + timedelta(days=n)
        for n in range((fecha_salida - fecha_entrada).days + 1)
    ):
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
            print(
                f"🚫 La fecha {fecha.strftime('%Y-%m-%d')} no existe en el calendario de la habitación '{habitacion}'."
            )
            return None, None

    return fechas_a_reservar, fechas_no_disponibles


# Función para confirmar la reserva
def confirmar_reserva(
    fechas_a_reservar,
    habitacion,
    calendario,
    clientes,
    dni,
    fecha_entrada,
    fecha_salida,
    archivo_calendario,
):
    while True:
        confirmar = input("¿Deseas confirmar la reserva? (s/n): ").lower()
        if confirmar == "s":
            # Marcar las fechas como reservadas en el calendario
            for fecha in fechas_a_reservar:
                for i in range(len(calendario[habitacion])):
                    if calendario[habitacion][i][0].date() == fecha.date():
                        calendario[habitacion][i] = (
                            calendario[habitacion][i][0],
                            "reservado",
                        )

            # Guardar la reserva del cliente
            if "reservas" not in clientes[dni]:
                clientes[dni]["reservas"] = []

            clientes[dni]["reservas"].append(
                {
                    "habitacion": habitacion,
                    "fecha_entrada": fecha_entrada.strftime("%Y-%m-%d"),
                    "fecha_salida": fecha_salida.strftime("%Y-%m-%d"),
                    "dias": (fecha_salida - fecha_entrada).days,
                    "fechas_reservadas": [
                        fecha.strftime("%Y-%m-%d") for fecha in fechas_a_reservar
                    ],
                }
            )

            # Guardar clientes en el archivo
            guardar_clientes("clientes.json", clientes)
            # Guardar el calendario actualizado con las nuevas reservas
            guardar_calendario(archivo_calendario, calendario)
            print("✅ Reserva confirmada.")
            break
        elif confirmar == "n":
            print("❌ Reserva cancelada.")
            break


def buscar_reserva(archivo_clientes):
    imprimir_separador("🔍 Buscar Reserva por DNI 🔍")
    clientes = cargar_clientes(archivo_clientes)
    dni = int(input("Introduce tu DNI: "))
    cliente = clientes.get(str(dni))

    if not cliente or not cliente["reservas"]:
        print(f"❌ No se encontraron reservas activas para el DNI {dni}.")
        return

    # Mostrar todas las reservas del cliente
    imprimir_separador(f"Reservas para el DNI {dni}:")
    for i, reserva in enumerate(cliente["reservas"], 1):
        print(f"🔹 Reserva {i}:")
        print(f"   🏨 Habitación: {reserva['habitacion']}")
        print(f"   📅 Fecha de entrada: {reserva['fecha_entrada']}")
        print(f"   📅 Fecha de salida: {reserva['fecha_salida']}")
        print("   📆 Fechas reservadas:")
        for fecha in reserva["fechas_reservadas"]:
            print(f"      - {fecha}")
    imprimir_separador("Fin de reservas.")


# Función para convertir un objeto datetime a una cadena de texto
def fecha_a_str(fecha):
    return fecha.strftime("%Y-%m-%d")


# Función para convertir una cadena de texto a un objeto datetime
def str_a_fecha(fecha_str):
    return datetime.strptime(fecha_str, "%Y-%m-%d")


# Función para generar el calendario de habitaciones si no existe
def generar_calendario_por_habitaciones(
    inicio, fin, habitaciones, calendario_existente
):
    calendario = calendario_existente if calendario_existente else {}

    for habitacion in habitaciones:
        if habitacion not in calendario:
            calendario[habitacion] = [
                (inicio + timedelta(days=i), "disponible")
                for i in range((fin - inicio).days + 1)
            ]
    return calendario


# Función para cargar el calendario desde el archivo
def cargar_calendario(archivo_calendario):
    try:
        with open(archivo_calendario, "r") as f:
            calendario = json.load(f)
            # Convertir las fechas de nuevo a objetos datetime
            for habitacion, fechas in calendario.items():
                for i, (fecha_str, estado) in enumerate(fechas):
                    calendario[habitacion][i] = (str_a_fecha(fecha_str), estado)
            return calendario
    except (FileNotFoundError, json.JSONDecodeError):
        print(
            "El archivo de calendario no existe o está dañado. Creando calendario nuevo."
        )
        return {}


# Función para guardar el calendario actualizado
def guardar_calendario(archivo_calendario, calendario):
    try:
        calendario_serializado = {}
        for habitacion, fechas in calendario.items():
            calendario_serializado[habitacion] = [
                (fecha_a_str(fecha), estado) for fecha, estado in fechas
            ]

        with open(archivo_calendario, "w") as f:
            json.dump(calendario_serializado, f, indent=4)
        print("✅ Calendario guardado correctamente.")
    except Exception as e:
        print(f"❌ Error al guardar el calendario: {e}")


# Función para realizar la reserva (ajustada para trabajar con el calendario persistido)
def realizar_reserva(calendario, archivo_clientes, archivo_calendario):
    imprimir_separador("🏨 Realizar Reserva 🏨")

    habitaciones_disponibles = mostrar_habitaciones_disponibles(calendario)
    if not habitaciones_disponibles:
        return

    habitacion = input("Introduce el nombre de la habitación que deseas reservar: ")
    if habitacion not in habitaciones_disponibles:
        print(f"La habitación '{habitacion}' no está disponible.")
        return

    clientes = cargar_clientes(archivo_clientes)

    dni = solicitar_dni()

    if verificar_reserva_existente(dni, habitacion, clientes):
        return

    clientes = solicitar_dni_cliente(dni, clientes)

    # Mostrar el calendario de la habitación seleccionada, organizado por mes
    imprimir_separador(f"📅 Calendario de la Habitación {habitacion} 📅")
    fechas_habitacion = calendario.get(habitacion, [])

    if fechas_habitacion:
        # Crear un diccionario donde las claves son los meses y los valores son listas de fechas
        meses = {}
        for fecha, estado in fechas_habitacion:
            mes = fecha.strftime("%Y-%m")
            if mes not in meses:
                meses[mes] = []
            meses[mes].append(
                f"{fecha.strftime('%Y-%m-%d')} {'✔' if estado == 'disponible' else '❌'}"
            )

        # Imprimir las fechas organizadas por mes
        for mes, fechas in meses.items():
            imprimir_separador(
                f"✨ {datetime.strptime(mes, '%Y-%m').strftime('%B %Y')} ✨"
            )
            # Agrupar las fechas en bloques de 7 por línea para mejor visualización
            for i in range(0, len(fechas), 7):
                print("  ".join(fechas[i : i + 7]))
    else:
        print("No hay fechas disponibles en el calendario.")

    fecha_entrada = solicitar_fecha("Introduce la fecha de entrada")
    fecha_salida = solicitar_fecha("Introduce la fecha de salida")

    fecha_entrada, fecha_salida = validar_fechas(fecha_entrada, fecha_salida)

    fechas_a_reservar, fechas_no_disponibles = comprobar_disponibilidad_fechas(
        fecha_entrada, fecha_salida, habitacion, calendario
    )

    if fechas_a_reservar:
        print("\nDías disponibles para la reserva:")
        for fecha in fechas_a_reservar:
            print(f"  - {fecha.strftime('%Y-%m-%d')}")

    if fechas_no_disponibles:
        print("\nDías no disponibles:")
        for fecha in fechas_no_disponibles:
            print(f"  - {fecha.strftime('%Y-%m-%d')}")

    if not fechas_a_reservar:
        print("❌ No hay días disponibles en el rango seleccionado.")
        return

    # Confirmar la reserva
    confirmar_reserva(
        fechas_a_reservar,
        habitacion,
        calendario,
        clientes,
        dni,
        fecha_entrada,
        fecha_salida,
        archivo_calendario,
    )


def verificar_disponibilidad_avanzada(calendario, habitacion, fecha_inicio, fecha_fin):
    try:
        imprimir_separador(f"📋 Verificando Disponibilidad para {habitacion} 📋")

        fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
        fecha_fin = datetime.combine(fecha_fin, datetime.max.time())

        fechas_rango = list(
            filter(lambda x: fecha_inicio <= x[0] <= fecha_fin, calendario[habitacion])
        )

        dias_disponibles = reduce(
            lambda acc, x: acc + 1 if x[1] == "disponible" else acc, fechas_rango, 0
        )

        matriz = [[fecha[0].strftime("%Y-%m-%d"), fecha[1]] for fecha in fechas_rango]

        print(
            f"Días disponibles en el rango {fecha_inicio.date()} - {fecha_fin.date()}: {dias_disponibles}"
        )
        print("Detalles de la disponibilidad:")
        for dia in matriz:
            print(
                f"Fecha: {dia[0]} - Estado: {'✔' if dia[1] == 'disponible' else '❌'}"
            )

        return dias_disponibles
    except KeyError:
        print(f"⚠ La habitación '{habitacion}' no existe en el calendario.")
    except Exception as e:
        print(f"❌ Error al verificar disponibilidad: {e}")


4


def validar_habitacion(habitacion):
    return bool(re.fullmatch(r"[A-Z]\d{3}", habitacion.strip()))


def solicitar_habitacion(habitaciones):
    while True:
        habitacion = input(
            f"Introduce el nombre de la habitación ({', '.join(habitaciones)}): "
        ).strip()
        if validar_habitacion(habitacion) and habitacion in habitaciones:
            return habitacion
        print("⚠ Habitación inválida o no disponible.")


# Función principal para realizar la reserva
def main():
    archivo_usuarios = "usuarios.json"
    archivo_clientes = "clientes.json"
    archivo_calendario = "calendario.json"

    dni_usuario = autenticar_usuario(archivo_usuarios)
    if dni_usuario is None:
        return

    # Cargar calendario existente (si existe)
    calendario_existente = cargar_calendario(archivo_calendario)

    # Inicializar calendario y habitaciones, combinando con el calendario existente
    habitaciones = ["A101", "A102", "B101", "B102"]
    inicio = datetime(2024, 1, 1)
    fin = datetime(2026, 12, 31)
    calendario = generar_calendario_por_habitaciones(
        inicio, fin, habitaciones, calendario_existente
    )

    while True:
        imprimir_separador("🌟 Menú de Opciones 🌟")
        print("1. Realizar reserva")
        print("2. Buscar reserva por DNI")
        print("3. Mostrar calendario de una habitación")
        print("4. Verificar disponibilidad en rango de fechas")
        print("5. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            realizar_reserva(calendario, archivo_clientes, archivo_calendario)
        elif opcion == "2":
            buscar_reserva(archivo_clientes)
        elif opcion == "3":
            mostrar_calendario_habitacion(calendario, habitaciones, inicio, fin)
        elif opcion == "4":
            habitacion = solicitar_habitacion(habitaciones)
            fecha_inicio = solicitar_fecha("Introduce la fecha de inicio")
            fecha_fin = solicitar_fecha("Introduce la fecha de fin")
            if fecha_inicio > fecha_fin:
                print("⚠ La fecha de inicio no puede ser posterior a la fecha de fin.")
                continue
            verificar_disponibilidad_avanzada(
                calendario, habitacion, fecha_inicio, fecha_fin
            )
        elif opcion == "5":
            print("👋 Hasta pronto!")
            break
        else:
            print("⚠ Opción inválida.")


main()