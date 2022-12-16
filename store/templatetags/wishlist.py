from django import template
from store.models import Wishlist
register = template.Library()

@register.filter
def is_in_wishlist(self,user):
    try:
        wishlist = Wishlist.objects.get(user=user,product=self)
        return True
    except:
        return False

