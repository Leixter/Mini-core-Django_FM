from django.shortcuts import render
from .models import Venta, Regla, Vendedor  # <-- ¡Agregamos Vendedor aquí!
from decimal import Decimal
from collections import defaultdict
from django.http import HttpResponse
from datetime import date

def filtrar_ventas(request):
    resultados = []
    fecha_inicio = None
    fecha_fin = None

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            ventas = Venta.objects.filter(fecha_venta__range=[fecha_inicio, fecha_fin])

            # Sumar ventas por vendedor
            total_por_vendedor = defaultdict(Decimal)

            for venta in ventas:
                vendedor = venta.Vendedor
                total_por_vendedor[vendedor] += venta.monto

            # Obtener todas las reglas ordenadas por monto_minimo ASC
            reglas = Regla.objects.order_by('monto_minimo')

            for vendedor, total_ventas in total_por_vendedor.items():
                porcentaje_aplicado = 0

                # Buscar la regla correcta según el total vendido
                for regla in reglas:
                    if total_ventas >= regla.monto_minimo:
                        porcentaje_aplicado = regla.porcentaje

                comision = total_ventas * (Decimal(porcentaje_aplicado) / Decimal('100'))

                resultados.append({
                    'vendedor': vendedor.nombre,
                    'total_ventas': total_ventas,
                    'porcentaje': porcentaje_aplicado,
                    'comision': round(comision, 2)
                })

    return render(request, 'minicoreapp/filtro_ventas.html', {
        'resultados': resultados,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })

def inyectar_datos(request):
    r12, _ = Regla.objects.get_or_create(porcentaje=12.0, monto_minimo=1000.00)
    r8, _ = Regla.objects.get_or_create(porcentaje=8.0, monto_minimo=0.00)

    v1, _ = Vendedor.objects.get_or_create(nombre='Perico P')
    v2, _ = Vendedor.objects.get_or_create(nombre='Zoila Baca')
    v3, _ = Vendedor.objects.get_or_create(nombre='Aquiles C')

    f_venta = date(2025, 5, 15)

    Venta.objects.get_or_create(Vendedor=v1, regla=r12, fecha_venta=f_venta, monto=1200.00)
    Venta.objects.get_or_create(Vendedor=v2, regla=r8, fecha_venta=f_venta, monto=800.00)
    Venta.objects.get_or_create(Vendedor=v3, regla=r8, fecha_venta=f_venta, monto=900.00)

    return HttpResponse("¡Magia hecha! Datos insertados correctamente en Render.")
