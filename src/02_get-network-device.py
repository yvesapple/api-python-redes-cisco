import json
import requests
api_url = "http://localhost:58000/api/v1/network-device"

headers = {"X-Auth-Token": "NC-6-988d31f0a743413db264-nbi"}

resp = requests.get(api_url, headers=headers)

print("Request status: ", resp.status_code)

response_json = resp.json()
print()
print()
print(response_json)
print()
print()

# Usamos .get() por si la llave "response" no viene en el JSON
networkDevices = response_json.get("response", [])

print("Dispositivos de Red (ignorando los que no tienen hostname):")
print("-" * 60)

for networkDevice in networkDevices:
    # Buscamos el hostname. Si no existe, devuelve una cadena vacía.
    hostname = networkDevice.get("hostname", "")
    
    # Si el hostname está vacío (como el ISP o el Controller), lo salteamos
    if not hostname:
        continue
        
    # Usamos .get() para los otros campos por seguridad
    platform = networkDevice.get("platformId", "N/A")
    ip = networkDevice.get("managementIpAddress", "N/A")
    
    print(hostname, "\t", platform, "\t", ip)