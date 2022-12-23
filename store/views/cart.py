from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from store.models import Order, OrderItem, Product, Wishlist
from shop import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import razorpay
import os
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
# Create your views here.

client = razorpay.Client(auth=(settings.razor_pay_key_id, settings.key_secret))

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

@login_required(login_url='/login')
def user_wishlist(request,slug):
    user = User.objects.get(username=request.user.username)
    product = Product.objects.get(slug=slug)
    try:
        print(product)
        existing_wishlist = Wishlist.objects.get(user=user,product=product)
        print(existing_wishlist)
        existing_wishlist.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        wishlist =Wishlist.objects.create(user=user,product=product)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def view_wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    context = {'wishlists':wishlists}
    return render(request,'store/wishlist.html',context)

def checkout(request):

 
    return render(request,'store/checkout.html')

@login_required(login_url='/login')
def place_order(request):
    amount =  int(request.POST.get("amount"))
    print(amount)
    data = { "amount":amount*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    context = {
        'payment':payment,
        'key_id':settings.razor_pay_key_id
    }
    print(context)

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    country =  request.POST.get('country')
    address = request.POST.get('address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    postcode = request.POST.get('postcode')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    additional_info = request.POST.get('additional_info')
    amount = data.get('amount')
    order_id =payment['id']
    
    order = Order.objects.create(
        user = User.objects.get(pk=request.user.pk),
        first_name=first_name,
        last_name=last_name,
        country=country,
        address=address,
        city=city,
        state=state,
        postcode=postcode,
        phone=phone,
        email=email,
        additional_info=additional_info,
        amount=amount,
        order_id=order_id,
    )
    order.save()

    cart = request.session.get('cart')
    for item in cart:
        order_id = OrderItem.objects.create(
            order = order,
            product = cart[item]['name'],
            image = cart[item]['image'],
            price = cart[item]['price'],
            total = str(int(cart[item]['price'])*int(cart[item]['quantity'])),
            quantity = cart[item]['quantity']
        )
    print(cart)
    print('cart')
    return render(request,'store/place_order.html',context)



def fetch_resources(uri,rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

from django.contrib.staticfiles import finders


def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # response = HttpResponse(content_type='application/pdf')
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required(login_url='/login')
def success(request):
    order_id = request.GET.get('order_id')
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_signature = request.GET.get('razorpay_signature')

    order = Order.objects.get(order_id=order_id)
    order.razorpay_payment_id = razorpay_payment_id
    order.razorpay_signature = razorpay_signature
    order.paid = "True"
    order.save()
    cart = Cart(request)
    cart.clear()
    data = {
        'order_id':order_id,
        'payment_id':razorpay_payment_id,
        'order':order,
        'total_amount':int(order.amount)/100,
    }
    pdf = render_to_pdf('payment/invoice.html',data)
    print(pdf,'dfsdd')
    if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
    return HttpResponse("Not found")
    # return HttpResponse(pdf,content_type='application/pdf')
@login_required(login_url='/login')
def order_detail(request,pk):
    order_item = OrderItem.objects.get(pk=pk)
    context = {'order_item':order_item}
    return render(request,'account/order_detail.html',context)
