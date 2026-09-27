from datetime import datetime


VALOR_CITA = {
    "Particular": 80000,
    "EPS": 5000,
    "Prepagada": 30000,
}

VALOR_ATENCION = {
    "Particular":{
        "Limpieza": 60000,
        "Calzas": 80000,
        "Extracción": 100000,
        "Diagnóstico": 50000,

    },
    "EPS":{
        "Limpieza": 0,
        "Calzas": 40000,
        "Extracción": 40000,
        "Diagnóstico": 0,

    },
    "Prepagada": {
        "Limpieza": 0,
        "Calzas": 10000,
        "Extracción": 10000,
        "Diagnóstico": 0,
    },

}

TIPOS_CLIENTE =["Particular", "EPS", "Prepagada"]
TIPOS_ATENCION =["Limpieza", "Calzas", "Extracción", "Diagnóstico"]
PROPIEDADES = ["Normal", "Urgente"]

def formato_pesos(valor):
    texto = f"{valor:,}"
    texto = texto.replace(",", ".")
    return "$" + texto 

def leer_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        print("ERROR: Este dato es obligatorio.")
        texto = input(mensaje).strip()
    return texto


def leer_digitos(mensaje):
    texto = input(mensaje).strip()
    while texto == "" or not texto.isdigit():
        print("ERROR: Este dato es obligatorio y solo se permiten números.")
        texto = input(mensaje).strip()
    return texto



def elegir_opcion(titulo, opciones):
    print (titulo)
    for i in range(len(opciones)):
        print(f" {i + 1}. {opciones[i]}")
    eleccion = input("Elija una opcion: ").strip()
    while not (eleccion.isdigit() and 1 <= int(eleccion)
<= len(opciones)):
        print ("ERROR: la opcion no es valida. ")
        eleccion = input("Elija una opción: ").strip()
    return opciones[int(eleccion) - 1]

def leer_cantidad(tipo_atencion):
    if tipo_atencion == "Limpieza" or tipo_atencion == "Diagnostico":
        print("  Cantidad: 1 (Siempre es1 para este tipo de atencion)")
        return 1
    cantidad = input("Cantidad: ").strip()
    while not (cantidad.isdigit() and int (cantidad) > 0):
        print(" La cantidad debe ser un numero entero mayor que cero.")
        cantidad = input("Cantidad: ").strip()
    return int(cantidad)


def calcular_valor(tipo_cliente, tipo_atencion, cantidad):
    valor_cita = VALOR_CITA[tipo_cliente]
    valor_atencion = VALOR_ATENCION[tipo_cliente][tipo_atencion]
    valor_pagar = valor_cita + valor_atencion * cantidad
    return valor_pagar

def registrar_cliente ():
    print("\n--- Nuevo Cliente ---")
    cedula = leer_digitos("Cedula: ")
    nombre = leer_texto("Nombre: ").lower()
    telefono = leer_digitos ("Teléfono: ")
    tipo_cliente = elegir_opcion ("Tipo de cliente:", TIPOS_CLIENTE)
    tipo_atencion = elegir_opcion ("Tipo de atencion:", TIPOS_ATENCION)
    cantidad = leer_cantidad(tipo_atencion)
    prioridad = elegir_opcion ("Prioridad de atencion:", PROPIEDADES)
    fecha = leer_texto ("Fecha de la cita (DD/MM/AAAA):")

    valor_pagar = calcular_valor(tipo_cliente, tipo_atencion, cantidad)
    print(f"Valor a pagar: {formato_pesos(valor_pagar)}")

    cliente = {
        "cedula": cedula,
        "nombre": nombre,
        "telefono": telefono,
        "tipo_cliente": tipo_cliente,
        "tipo_atencion": tipo_atencion,
        "cantidad": cantidad,
        "prioridad": prioridad,
        "fecha": fecha,
        "valor_pagar": valor_pagar,
    }
    return cliente

def calcular_resumen(clientes):
    total_clientes = len(clientes)
    ingresos = 0 
    extracciones = 0 
    for cliente in clientes:
        ingresos += cliente["valor_pagar"]
        if cliente["tipo_atencion"] == "Extracción":  # con tilde
            extracciones += 1
    return total_clientes, ingresos, extracciones



def ordenar_por_valor(clientes):
    lista = clientes.copy()
    n = len(lista)
    for i in range (n - 1):
        for j in range (n - 1 - i):
            if lista[j]["valor_pagar"] < lista [j + 1] ["valor_pagar"]:
                aux = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = aux
    
    return lista

def mostrar_clientes(lista):
    posicion = 1
    for cliente in lista:
        print(f"{posicion}. {cliente['nombre']} (cédula {cliente['cedula']})")
        print(f"   {cliente['tipo_cliente']} - {cliente['tipo_atencion']} x {cliente['cantidad']}")
        print(f"   Valor a pagar: {formato_pesos(cliente['valor_pagar'])}")
        posicion = posicion + 1


def buscar_por_cedula(lista, cedula):
    for cliente in lista:
        if cliente["cedula"] == cedula:
            return cliente
    return None

def main():
    print("=== Consultorio odontológico ===")

    # 1. Registrar varios clientes en la lista
    clientes = []
    otro = "s"
    while otro == "s":
        cliente = registrar_cliente()
        clientes.append(cliente)
        otro = input("\n¿Registrar otro cliente? (s/n): ").strip().lower()

    
    total_clientes, ingresos, extracciones = calcular_resumen(clientes)
    print("\n=== Resumen ===")
    print(f"Total clientes: {total_clientes}")
    print(f"Ingresos totales: {formato_pesos(ingresos)}")
    print(f"Clientes para extracción: {extracciones}")

    ordenados = ordenar_por_valor(clientes)
    print("\n=== Clientes ordenados por valor a pagar (mayor a menor) ===")
    mostrar_clientes(ordenados)

    cedula = leer_digitos("\nCédula a buscar: ")
    encontrado = buscar_por_cedula(ordenados, cedula)
    if encontrado is None:
        print("No se encontró un cliente con esa cédula.")
    else:
        print("\nCliente encontrado:")
        print(f"  Nombre: {encontrado['nombre']}")
        print(f"  Teléfono: {encontrado['telefono']}")
        print(f"  Tipo de cliente: {encontrado['tipo_cliente']}")
        print(f"  Atención: {encontrado['tipo_atencion']} x {encontrado['cantidad']}")
        print(f"  Prioridad: {encontrado['prioridad']}")
        print(f"  Fecha: {encontrado['fecha']}")
        print(f"  Valor a pagar: {formato_pesos(encontrado['valor_pagar'])}")


main()