#Módulos que se usarán
import requests #Para entender solicitudes
import json #Para reconocer el formato json
from tabulate import * #Para crear tablas

baseUri = "http://localhost:58000/api/v1" #URL de PT

# Llamada al API por el ticket
headers = {"Content-Type": "application/json"} #Headers
data = json.dumps({"username": "cisco", "password": "class"}) #Credenciales
resp = requests.post(baseUri+"/ticket", data=data, headers=headers) #URL específica

print("Status de Solicitud:")
print(resp.status_code)
result = resp.json()
# print(result)

ticket = result["response"]["serviceTicket"] #Printing ticket
print("\nEl Service Ticket es:")
print(ticket)


# Llamada al API para recibir los dispositivos de red
headers = {"X-Auth-Token": ticket}
resp = requests.get(baseUri+"/network-device", headers=headers) #URL específica

# print (resp.status_code)
result = resp.json()
#print (json.dumps(result, indent=4))
print("\nDispositivos de Red:")
host_list=[]
i=0
for item in result["response"]:
    # Usamos .get() para que no explote si falta el dato
    hostname = item.get("hostname", "") 
    
    # Si el hostname está vacío (es decir, no lo tiene), saltamos este dispositivo
    if not hostname:
        continue 
        
    i+=1
    # También usamos .get() para los otros campos por las dudas
    serial = item.get("serialNumber", "N/A")
    version = item.get("softwareVersion", "N/A")
    
    host_list.append([i, hostname, serial, version])

print(tabulate(host_list,headers=["Hostname","Serial Number","Software Version"],tablefmt='rst')) #Tabla ordenada 

# Llamada al API para recibir los host
headers = {"X-Auth-Token": ticket }
resp = requests.get(baseUri+"/host", headers=headers) #URL específica

# print (resp.status_code)
result = resp.json()
#print (json.dumps(result, indent=4))
print("\nHosts de la Red:")
host_list=[]
i=0
for item in result["response"]:
    i+=1
    host_list.append([i,item["hostName"],item["hostType"],item["hostIp"]])
    #print(item["hostName"]+" "+item["hostType"]+" "+item["hostIp"]) #Lista completa

print(tabulate(host_list,headers=["Hostname","Tipo","IP"],tablefmt='rst')) #Tabla ordenada 