from django.urls import path
from . import views # el . significa directorio actual

app_name = "app_contabilidad_inversiones"
urlpatterns = [
    path("", views.index, name="index"),
    path("resumen", views.resumen_inversiones, name="resumen_inversiones"),
    path("nueva_transaccion", views.ingresar_transaccion, name="ingresar_transaccion"),
    path("transacciones", views.ver_transacciones, name="ver_transacciones"),
    path("informe_detallado", views.ver_informe_detallado, name="ver_informe_detallado"),
    path("eliminar_transaccion", views.eliminar_transaccion, name="eliminar_transaccion"),
]