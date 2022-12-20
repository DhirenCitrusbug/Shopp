from django import template
from store.models import Compare
register = template.Library()

@register.filter
def is_in_compare(self,user):
    try:
        Compare.objects.get(user=user,product=self)
        return True
    except:
        return False

