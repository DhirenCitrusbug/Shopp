from django.shortcuts import redirect, render
from . models import Product, Category, FilterPrice, Color, Brand, Contact
from shop import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
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
    search = request.POST.get('search')
    if request.method == "POST":
        if search:
            products = Product.objects.filter(name__icontains=search)
    context = {'products':products,'search':search}
    return render(request,'store/search.html',context)


def product_detail(request,slug):
    product = Product.objects.filter(slug=slug)
    print(product,'====================')
    context = {'product':product[0]}
    return render(request,'store/product_detail.html',context)

def contact(request):
    if request.method == 'POST': 
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact.objects.create(name=name,email=email,subject=subject,message=message)
        contact.save()
        from django.core.mail import send_mail
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return redirect('/')
    return render(request,'store/contact.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password==cpassword:
            user = User.objects.create(username=username, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
            messages.warning(request,"Confirm Password Not Mached")
    return render(request,'store/login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.warning(request,"Invalid Credentials")
    return render(request,'store/login.html')

def logout(request):
    user = request.user
    if user:
        auth.logout(request)
    return redirect('login')



@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'store/cart.html')

def checkout(request):
    return render(request,'store/checkout.html')