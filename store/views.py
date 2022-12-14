from django.shortcuts import render
from . models import Product, Category, FilterPrice, Color, Brand
# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'store/index.html',context)

def products(request):
    if request.GET.get('selected_category'):

        category = Category.objects.get(slug=request.GET.get('selected_category'))
        products = Product.objects.filter(category=category)

    elif request.GET.get('selected_price'):
        selected_price = FilterPrice.objects.get(slug=request.GET.get('selected_price'))
        products = Product.objects.filter(filter_price=selected_price)

    elif request.GET.get('selected_color'):
        selected_color = Color.objects.get(slug=request.GET.get('selected_color'))
        products = Product.objects.filter(color=selected_color)

    elif request.GET.get('selected_brand'):
        selected_brand = Brand.objects.get(slug=request.GET.get('selected_brand'))
        products = Product.objects.filter(brand=selected_brand)

    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    price_filter = FilterPrice.objects.all()
    colors = Color.objects.all()
    brands = Brand.objects.all()
    print('=============',request.GET)
    if request.GET.get('sortby'):
        print(products)

        sortby = request.GET.get('sortby')
        if sortby=='AtoZ':
            products = products.order_by('name')
        elif sortby=='ZtoA':
            products = products.order_by('-name')
            print(products)
        elif sortby=='ascending-price':
            products = products.order_by('price')
            print(products)
        elif sortby=='decending-price':
            products = products.order_by('-price')

    context = {'products':products,'categories':categories,'products_count':Product.objects.all().count()}
    context['price_filter']=price_filter
    context['colors']=colors
    context['brands']=brands

    return render(request,'store/products.html',context)


def search(request):
    products = Product.objects.all()
    if request.method == "POST":
        search = request.POST.get('search')
        if search:
            products = Product.objects.filter(name__icontains=search)
    context = {'products':products}
    return render(request,'store/search.html',context)