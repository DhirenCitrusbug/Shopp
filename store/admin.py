from django.contrib import admin
from .models import *
# Register your models here.

class ImageTublerInine(admin.TabularInline):
    model = Image

class TagTublerInine(admin.TabularInline):
    model = Tag   

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageTublerInine,TagTublerInine]
class OrderTublerInine(admin.TabularInline):
    model = Order

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderTublerInine,]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(FilterPrice)
admin.site.register(Product,ProductAdmin)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)

