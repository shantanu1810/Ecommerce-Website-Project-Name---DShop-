from django import template

register = template.Library()

@register.filter
def to_float(value):
    print(type(value)," ",value)
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
    
@register.filter
def discount(price,dis):
    try:
        value=float(price)-float(float(price)*float(dis)/100)
        value=round(value)
        return value
    except (ValueError, TypeError):
        return ''
@register.filter
def slice(detail,n):
    try:
        d=int(n)
        return ' '.join(detail[d:])
    except (ValueError, TypeError):
        return ''
    
@register.filter
def substring(detail,n):
    try:
        d=int(n)
        return detail[d:]
    except (ValueError, TypeError):
        return ''