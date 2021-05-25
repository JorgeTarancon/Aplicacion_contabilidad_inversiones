#################################### IMPORTS ####################################
from .models import Transacciones, Plataformas_inversion
import requests
from django.db.models import Count
from datetime import datetime
#################################### IMPORTS ####################################

def obtener_resumen_por_plataforma(unidades):
    json_conversion = conectarse_api_currency_exchange()
    pt=Plataformas_inversion.objects.all()
    transacciones_por_plataforma,dinero_por_plataforma,plataformas = [],[],[]
    for i in range(len(pt)):
        plataformas.append(pt[i].nombre_plataforma)
        transacciones = Transacciones.objects.filter(plataforma=pt[i].id).values('precio','moneda')
        transacciones_por_plataforma.append(len(transacciones))
        suma = 0
        for t in range(len(transacciones)):
            precio,moneda = convertir_precio_moneda(unidades,transacciones[t]['moneda'],float(transacciones[t]['precio']),json_conversion)
            suma += precio
        dinero_por_plataforma.append(suma)
    return plataformas,transacciones_por_plataforma,dinero_por_plataforma

def obtener_fecha_numero_transacciones():
    ts = Transacciones.objects.values('fecha').order_by('fecha').annotate(count=Count('fecha'))
    fechas,conteo = [],[]
    for i in range(len(ts)):
        fechas.append( ts[i]['fecha'].strftime('%d-%m-%Y') )
        conteo.append(ts[i]['count'])
    return fechas,conteo

def conectarse_api_currency_exchange():
    with open('./claves.txt','r') as file: api = eval(file.read())['api_exchange_rates']
    response = requests.get(api)
    if response.status_code == 200:
        return response.json()['rates']
    else: return 'Error'

def conectarse_yahoo_finance(symbol,bolsa):
    with open('./claves.txt','r') as file: api = eval(file.read())['yahoo_finance']
    response = requests.get(api+symbol+'.'+bolsa)
    if response.status_code == 200:
        response = response.json()['quoteResponse']['result'][0]
        return response['regularMarketPrice'],response['currency']
    else: return 'Error'

def obtener_precio_actual_transacciones(moneda_mostrar):
    ts = Transacciones.objects.exclude(bolsa__isnull=True).values('nombre','simbolo','bolsa')
    diccionario = {}
    json_conversion = conectarse_api_currency_exchange()
    for i in range(len(ts)):
        precio,moneda = conectarse_yahoo_finance(ts[i]['simbolo'],ts[i]['bolsa'])
        precio_convertido, moneda_convertida = convertir_precio_moneda(moneda_mostrar,moneda,precio,json_conversion)
        diccionario[ts[i]['simbolo']] = {
            'nombre':ts[i]['nombre'],
            'bolsa':ts[i]['bolsa'],
            'precio_actual': precio_convertido,
            'moneda':moneda_convertida
        }
    return diccionario

def convertir_precio_moneda(moneda_a_convertir,moneda_actual,precio_actual,json_conversion):
    if moneda_a_convertir == 'Original': precio_convertido,moneda_convertida = precio_actual,moneda_actual
    else:
        if moneda_actual == moneda_a_convertir:
            precio_convertido = round(float(precio_actual),2)
            moneda_convertida = moneda_actual
        else:
            if moneda_a_convertir == 'EUR':
                precio_convertido = round((float(precio_actual) / json_conversion[moneda_actual]),2)
            else:
                precio_convertido = round((float(precio_actual)*json_conversion[moneda_a_convertir]),2)
            moneda_convertida = moneda_a_convertir
    return precio_convertido, moneda_convertida