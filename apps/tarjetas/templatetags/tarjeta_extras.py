from django import template

register = template.Library()

tarjetas_con_iconos = ['visa', 'mastercard', 'americanexpress']

@register.filter
def get_icono(empresa):
    empresa = empresa.lower().replace(" ", "")
    return empresa if empresa in tarjetas_con_iconos else 'otras'
