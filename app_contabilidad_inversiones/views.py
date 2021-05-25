from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Transacciones, Plataformas_inversion
from django.db.models import Max,Min
from . import funciones_python as fj
import pandas as pd

# Create your views here.
posibles_monedas = (
                        ('Original','Original'),
                        ('EUR','EUR'),
                        ('USD','USD'),
                    )

#################################### CLASES ####################################
class NewTransactionForm(forms.Form):
    date = forms.DateField(label=False,#widget=forms.DateInput(format="%d/%m/%Y"),
                            widget=forms.DateInput(attrs={'placeholder':'Fecha: dd/mm/yyyy'}),
                            input_formats=("%d/%m/%Y",))
    activo = forms.CharField(label=False,
                                widget=forms.TextInput(attrs={'placeholder':"Nombre del activo"}))
    plataforma = forms.ChoiceField(label=False,
                                    choices=(
                                        ('DE GIRO','DE GIRO'),
                                        ('MINTOS','MINTOS'),
                                        ('AXA','AXA')
                                        ))
    moneda = forms.ChoiceField(label=False,
                                    choices=posibles_monedas[1:])
    simbolo = forms.CharField(label=False, required=False,
                                widget=forms.TextInput(attrs={'placeholder':"Símbolo"}))
    bolsa = forms.CharField(label=False, required=False,
                                widget=forms.TextInput(attrs={'placeholder':"Bolsa (Yahoo Finance)"}))

    precio_transaccion = forms.DecimalField(label=False,decimal_places=2,min_value=0,
                                            widget=forms.TextInput(attrs={'placeholder':"Precio"}))

class EliminarTransactionForm(forms.Form):
    id_transaccion_eliminar = forms.IntegerField(
                        min_value=int(Transacciones.objects.values('id').aggregate(Min('id'))['id__min']),
                        max_value=int(Transacciones.objects.values('id').aggregate(Max('id'))['id__max']))

class Elegir_Moneda_a_mostrar(forms.Form):
    moneda_mostrar = forms.ChoiceField(label=False,
                                    choices=posibles_monedas)
class Elegir_Moneda_a_mostrar_dos_opciones(forms.Form):
    moneda_mostrar = forms.ChoiceField(label=False,
                                    choices=posibles_monedas[1:])
#################################### CLASES ####################################

#################################### VISTAS ####################################
def index(request):
    return render(request, "app_contabilidad_inversiones/index.html")

#precio,moneda = fj.conectarse_yahoo_finance(symbol='VOO',bolsa='AS')
#return render(request, "",{
#    "precio":precio,
#    "moneda":moneda
#})

def resumen_inversiones(request):
    if request.method == "POST":
        form = Elegir_Moneda_a_mostrar_dos_opciones(request.POST)
        moneda_mostrar = [request.POST.get("moneda_mostrar")][0]    
    else:
        moneda_mostrar = 'EUR'
        form = Elegir_Moneda_a_mostrar_dos_opciones()
    numero_transacciones = len(Transacciones.objects.all())
    numero_plataformas = len(Plataformas_inversion.objects.all())
    fechas,conteo_por_fecha = fj.obtener_fecha_numero_transacciones()
    plataformas,transacciones,dinero_por_plataforma = fj.obtener_resumen_por_plataforma(moneda_mostrar)
    return render(request, "app_contabilidad_inversiones/resumen.html",{
        "form":form,
        "numero_transacciones":numero_transacciones,
        "numero_plataformas":numero_plataformas,
        "transacciones":transacciones,
        "plataformas":plataformas,
        "fechas":fechas,
        "conteo_por_fecha":conteo_por_fecha,
        "dinero_por_plataforma":dinero_por_plataforma,
        "moneda_mostrar":moneda_mostrar
    })

def ingresar_transaccion(request):
    if request.method == "POST": # Si pulsamos el boton de enviar
        form = NewTransactionForm(request.POST) # Cogemos lo que estaba en el formulario que hemos enviado
        if form.is_valid(): # Si los datos del formulario son validos, los guardamos en variables y vamos a la url indicada
            fecha_transaccion = form.cleaned_data["date"]
            nombre_activo = form.cleaned_data["activo"].upper()
            plataforma = Plataformas_inversion.objects.get(nombre_plataforma=form.cleaned_data["plataforma"])
            moneda = form.cleaned_data["moneda"]
            precio_transaccion = form.cleaned_data["precio_transaccion"]
            simbolo = form.cleaned_data["simbolo"]
            bolsa = form.cleaned_data["bolsa"]

            nueva_transaccion = Transacciones(fecha=fecha_transaccion,nombre=nombre_activo,simbolo=simbolo,bolsa=bolsa,plataforma=plataforma,moneda=moneda,precio=precio_transaccion)
            nueva_transaccion.save()

            return HttpResponseRedirect(reverse("app_contabilidad_inversiones:index"))
        else: return render(request, "app_contabilidad_inversiones/ingresar_transaccion.html",{
            "form": form
            }) # Si los datos del formulario no son validos, devolvemos a la misma pagina, con los mismos datos para que los cambien

    return render(request, "app_contabilidad_inversiones/ingresar_transaccion.html",{
        "form":NewTransactionForm() # Si no hacemos POST, solo queremos que nos muestre la pagina con el formulario vacio
    })

def ver_transacciones(request):
    if request.method == "POST":
        form = Elegir_Moneda_a_mostrar(request.POST)
        moneda_mostrar = [request.POST.get("moneda_mostrar")][0]
        diccionario = {}
        ts = Transacciones.objects.all().order_by("fecha")
        currency_exchange = fj.conectarse_api_currency_exchange()
        for i in range(len(ts)):
            precio_convertido,moneda_convertida = fj.convertir_precio_moneda(moneda_mostrar,ts[i].moneda,ts[i].precio,currency_exchange)
            diccionario[ts[i].id] = {
                                        "fecha":ts[i].fecha,
                                        "nombre":ts[i].nombre,
                                        "simbolo":'' if pd.isnull(ts[i].simbolo) else ts[i].simbolo,
                                        "bolsa": '' if pd.isnull(ts[i].bolsa) else ts[i].bolsa,
                                        "precio":precio_convertido,
                                        "moneda":moneda_convertida,
                                        "plafatorma":ts[i].plataforma.nombre_plataforma,
                                    }
        return render(request, "app_contabilidad_inversiones/transacciones.html",{
            "transacciones":Transacciones.objects.all().order_by("fecha"),
            "diccionario_transacciones":diccionario,
            "form":form,
        })
    else:
        return render(request, "app_contabilidad_inversiones/transacciones.html",{
            "transacciones":Transacciones.objects.all().order_by("fecha"),
            "form":Elegir_Moneda_a_mostrar()
        })

def ver_transaccion_individual(request,transaccion_id):
    if request.method == "POST":
        Transacciones.objects.get(pk=int(transaccion_id)).delete()
        return HttpResponseRedirect(reverse("app_contabilidad_inversiones:ver_transacciones"))
    transaccion = Transacciones.objects.get(pk=transaccion_id)
    return render(request, "app_contabilidad_inversiones/transaccion_individual.html",{
                "transaccion":transaccion
    })

def ver_cotizaciones_actuales(request):
    if request.method == "POST":
        form = Elegir_Moneda_a_mostrar_dos_opciones(request.POST)
        moneda_mostrar = [request.POST.get("moneda_mostrar")][0]    
    else:
        moneda_mostrar = 'EUR'
        form = Elegir_Moneda_a_mostrar_dos_opciones()
    diccionario_precio_actual_stocks = fj.obtener_precio_actual_transacciones(moneda_mostrar)
    return render(request, "app_contabilidad_inversiones/ver_cotizaciones_actuales.html",{
        "form":form,
        "diccionario_precio_actual_stocks":diccionario_precio_actual_stocks
    })
#################################### VISTAS ####################################