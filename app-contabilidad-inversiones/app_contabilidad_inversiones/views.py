from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Transacciones, Plataformas_inversion
from django.db.models import Max,Min

# Create your views here.

class NewTransactionForm(forms.Form):
    date = forms.DateField(label="Fecha",#widget=forms.DateInput(format="%d/%m/%Y"),
                            widget=forms.DateInput(attrs={'placeholder':'dd/mm/yyyy'}),
                            input_formats=("%d/%m/%Y",))
    activo = forms.CharField(label="Nombre del activo")
    plataforma = forms.ChoiceField(label="Plataforma de inversión",
                                    choices=(
                                        ('DE GIRO','DE GIRO'),
                                        ('MINTOS','MINTOS'),
                                        ('AXA','AXA')
                                        ))
    precio_transaccion = forms.DecimalField(label="Precio (€)",decimal_places=2,min_value=0)

class EliminarTransactionForm(forms.Form):
    id_transaccion_eliminar = forms.IntegerField(
                        min_value=int(Transacciones.objects.values('id').aggregate(Min('id'))['id__min']),
                        max_value=int(Transacciones.objects.values('id').aggregate(Max('id'))['id__max']))

def index(request):
    return render(request, "app_contabilidad_inversiones/index.html")

    #return render(request, "app_contabilidad_inversiones/index.html")

def resumen_inversiones(request):
    return render(request, "app_contabilidad_inversiones/resumen.html")

def ingresar_transaccion(request):
    if request.method == "POST": # Si pulsamos el boton de enviar
        form = NewTransactionForm(request.POST) # Cogemos lo que estaba en el formulario que hemos enviado
        if form.is_valid(): # Si los datos del formulario son validos, los guardamos en variables y vamos a la url indicada
            fecha_transaccion = form.cleaned_data["date"]
            nombre_activo = form.cleaned_data["activo"]
            plataforma = Plataformas_inversion.objects.get(nombre_plataforma=form.cleaned_data["plataforma"])
            precio_transaccion = form.cleaned_data["precio_transaccion"]
            
            nueva_transaccion = Transacciones(fecha=fecha_transaccion,nombre=nombre_activo,plataforma=plataforma,precio=precio_transaccion)
            nueva_transaccion.save()

            return HttpResponseRedirect(reverse("app_contabilidad_inversiones:index"))
        else: return render(request, "app_contabilidad_inversiones/ingresar_transaccion.html",{
            "form": form
            }) # Si los datos del formulario no son validos, devolvemos a la misma pagina, con los mismos datos para que los cambien

    return render(request, "app_contabilidad_inversiones/ingresar_transaccion.html",{
        "form":NewTransactionForm() # Si no hacemos POST, solo queremos que nos muestre la pagina con el formulario vacio
    })

def ver_transacciones(request):
    return render(request, "app_contabilidad_inversiones/transacciones.html",{
        "transacciones":Transacciones.objects.all()
    })

def ver_informe_detallado(request):
    return render(request, "app_contabilidad_inversiones/informe_detallado.html")

def eliminar_transaccion(request):
    if request.method=="POST":
        form = EliminarTransactionForm(request.POST)
        if form.is_valid():
            Transacciones.objects.get(pk=int(form.cleaned_data["id_transaccion_eliminar"])).delete()
            return HttpResponseRedirect(reverse("app_contabilidad_inversiones:index"))
        else: return render(request, "app_contabilidad_inversiones/ingresar_transaccion.html",{
            "form": form
            })
    return render(request, "app_contabilidad_inversiones/eliminar_transaccion.html",{
                "form":EliminarTransactionForm()
    })