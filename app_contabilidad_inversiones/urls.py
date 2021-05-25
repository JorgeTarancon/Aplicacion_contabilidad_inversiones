from django.urls import path
from . import views # el . significa directorio actual

app_name = "app_contabilidad_inversiones"
urlpatterns = [
    path("", views.index, name="index"),
    path("resumen", views.resumen_inversiones, name="resumen_inversiones"),
    path("nueva_transaccion", views.ingresar_transaccion, name="ingresar_transaccion"),
    path("transacciones", views.ver_transacciones, name="ver_transacciones"),
    path("<int:transaccion_id>",views.ver_transaccion_individual, name="ver_transaccion_individual"),
    path("cotizaciones",views.ver_cotizaciones_actuales, name="ver_cotizaciones_actuales")
]