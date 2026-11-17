# Documentación de Scripts API REST - Network Controller
Este documento detalla el funcionamiento de los scripts personalizados desarrollados en Python para interactuar con el Network Controller (Cisco DNA Center simulado en Packet Tracer) a través de su API REST.

## Requisitos previos
- Tener el entorno de Python configurado con las librerías requests y json.
- El Network Controller debe estar encendido y con el Discovery finalizado.

## Script 1: Buscador de Equipos (buscar-equipo.py)
### Descripción
Este script consulta el endpoint '/network-device' para obtener la lista completa de dispositivos descubiertos por el controlador. Permite al usuario buscar un equipo específico ingresando su Hostname o su Dirección IP de gestión. Una vez encontrado, muestra los datos principales (Nombre, Modelo e IP) por consola.
### Ejemplo de uso
```bash
python3 buscar-equipo.py
```
Salida esperada: El programa pedirá que se ingrese un nombre o IP (por ejemplo: Sucursal_2 o 192.168.99.1). Al encontrarlo, mostrará los datos en pantalla.

## Script 2: Obtención de Información Técnica (obtener-info-equipo.py)
### Descripción
Este script está diseñado para auditar un dispositivo específico en profundidad. Solicita al usuario el ingreso de una Dirección IP de gestión. Tras validarla contra la lista de dispositivos del controlador, extrae los datos técnicos del equipo (modelo, versión de software, número de serie y uptime) y genera un reporte detallado, exportandolo luego a csv.
### Ejemplo de uso
```bash
python3 obtener-info-equipo.py
```
Salida esperada: El programa solicitará la IP del equipo (ej: 192.168.92.1). Mostrará la ficha técnica en pantalla y generará el archivo detalle_equipo.csv.
