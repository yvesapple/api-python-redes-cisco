import json
import requests
import csv

base_url = "http://localhost:58000/api/v1"
credenciales = {"username": "cisco", "password": "class"}

# 1. Ticket
resp_ticket = requests.post(f"{base_url}/ticket", data=json.dumps(credenciales), headers={"Content-Type": "application/json"})
if resp_ticket.status_code != 201: exit("Error al obtener ticket")
ticket = resp_ticket.json()["response"]["serviceTicket"]
headers = {"X-Auth-Token": ticket}

# 2. Pedir la lista de todos los equipos
ip_equipo = input("Ingrese la IP del equipo para ver sus detalles: ").strip()
resp_dev = requests.get(f"{base_url}/network-device", headers=headers)

if resp_dev.status_code != 200:
    print("Error al consultar la lista de dispositivos.")
    exit()

dispositivos = resp_dev.json().get("response", [])
equipo_encontrado = None

# 3. Buscar el equipo en la lista
for d in dispositivos:
    if not isinstance(d, dict): continue
    if d.get("managementIpAddress") == ip_equipo:
        equipo_encontrado = d
        break

# 4. Mostrar los datos y exportar a CSV
if equipo_encontrado:
    # Guardamos los datos en variables para usarlos dos veces (consola y csv)
    hostname = equipo_encontrado.get('hostname', 'N/A')
    ip_gestion = equipo_encontrado.get('managementIpAddress', 'N/A')
    plataforma = equipo_encontrado.get('platformId', 'N/A')
    version = equipo_encontrado.get('softwareVersion', 'N/A')
    serial = equipo_encontrado.get('serialNumber', 'N/A')
    uptime = equipo_encontrado.get('upTime', 'N/A')

    # Mostrar por consola
    print(f"\n--- DETALLES DEL EQUIPO ---")
    print(f"Hostname: {hostname}")
    print(f"IP de Gestion: {ip_gestion}")
    print(f"Plataforma: {plataforma}")
    print(f"Version de Software: {version}")
    print(f"Numero de Serie: {serial}")
    print(f"Uptime: {uptime}")

    # Exportar a CSV
    nombre_archivo = "detalle_equipo.csv"
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        # Escribimos los encabezados
        escritor.writerow(["Hostname", "IP de Gestion", "Plataforma", "Version de Software", "Numero de Serie", "Uptime"])
        # Escribimos los datos del equipo
        escritor.writerow([hostname, ip_gestion, plataforma, version, serial, uptime])
        
    print(f"\nInformacion exportada exitosamente al archivo: {nombre_archivo}")

else:
    print("Equipo no encontrado.")