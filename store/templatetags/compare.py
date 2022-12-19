from django import template
from store.models import Compare
register = template.Library()

@register.filter
def is_in_compare(self,user):
    try:
        compare = Compare.objects.get(user=user,product=self)
        print(compare)
        return True
    except:
        print("Not")
        return False

