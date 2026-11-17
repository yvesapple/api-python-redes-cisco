import json
import requests
import csv

# ==========================================
# 1. OBTENER EL TICKET AUTOMÁTICAMENTE
# ==========================================
base_url = "http://localhost:58000/api/v1"
ticket_url = f"{base_url}/ticket"

credenciales = {"username": "cisco", "password": "class"}
headers_ticket = {"Content-Type": "application/json"}

print("Solicitando ticket al controlador...")
resp_ticket = requests.post(ticket_url, data=json.dumps(credenciales), headers=headers_ticket)

if resp_ticket.status_code == 201:
    ticket = resp_ticket.json()["response"]["serviceTicket"]
    print("Ticket obtenido correctamente.\n")
else:
    print(f"Error al obtener el ticket. Codigo: {resp_ticket.status_code}")
    print(resp_ticket.text)
    exit()

# ==========================================
# 2. OBTENER LOS DISPOSITIVOS DEL CONTROLADOR
# ==========================================
api_url = f"{base_url}/network-device"
headers = {"X-Auth-Token": ticket}

resp = requests.get(api_url, headers=headers)

if resp.status_code != 200:
    print(f"Error al consultar dispositivos. Codigo: {resp.status_code}")
    exit()

response_json = resp.json()
networkDevices = response_json.get("response", [])

# ==========================================
# 3. SOLICITAR DATO Y BUSCAR EL EQUIPO
# ==========================================
print("--- BUSCADOR DE DISPOSITIVOS (POR IP O HOSTNAME) ---")
busqueda = input("Ingrese la IP o el Hostname del equipo a buscar: ").strip()

# Variable para guardar el equipo si lo encontramos
equipo_encontrado = None

for networkDevice in networkDevices:
    if not isinstance(networkDevice, dict):
        continue
        
    ip_actual = networkDevice.get("managementIpAddress", "")
    hostname_actual = networkDevice.get("hostname", "")
    
    # Busca si la IP coincide exactamente O si el hostname coincide 
    # (Usamos lower() para que no importen las mayúsculas/minúsculas)
    if ip_actual == busqueda or hostname_actual.lower() == busqueda.lower():
        equipo_encontrado = networkDevice
        break # Cortamos el bucle porque ya lo encontramos

# ==========================================
# 4. MOSTRAR RESULTADO
# ==========================================
if equipo_encontrado:
    # Extraemos los datos
    hostname = equipo_encontrado.get("hostname", "N/A")
    platform = equipo_encontrado.get("platformId", "N/A")
    ip = equipo_encontrado.get("managementIpAddress", "N/A")
    
    print("\nEquipo encontrado:")
    print(f"Hostname: {hostname}")
    print(f"Modelo: {platform}")
    print(f"IP de gestion: {ip}")