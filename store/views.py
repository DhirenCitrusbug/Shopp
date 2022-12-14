# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect, render
# from .models import Compare, Order, OrderItem, Product, Category, FilterPrice, Color, Brand, Contact, Profile, Review, Wishlist
# from shop import settings
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib import auth
# from django.contrib.auth.decorators import login_required
# from cart.cart import Cart
# import razorpay
# import random
# from .task import send_otp

# # Create your views here.

# client = razorpay.Client(auth=(settings.razor_pay_key_id, settings.key_secret))

# def index(request):
#     # request.META['HTTP_CACHE_CONTROL']='no-cache'
#     # print(request.META['HTTP_CACHE_CONTROL'])
#     products = Product.objects.all()
#     context = {'products':products}
#     try:
#         wishlists = Wishlist.objects.filter(user=request.user)
#         request.session['wishlist_count'] = wishlists.count()
#         compares = Compare.objects.filter(user=request.user)
#         request.session['compare_count'] = compares.count()
#     except:
#         pass
#     return render(request,'store/index.html',context)

# def products(request):
#     if request.GET.get('selected_category'):

#         category = Category.objects.get(slug=request.GET.get('selected_category'))
#         products = Product.objects.filter(category=category)

#     elif request.GET.get('selected_price'):
#         selected_price = FilterPrice.objects.get(slug=request.GET.get('selected_price'))
#         products = Product.objects.filter(filter_price=selected_price)

#     elif request.GET.get('selected_color'):
#         selected_color = Color.objects.get(slug=request.GET.get('selected_color'))
#         products = Product.objects.filter(color=selected_color)

#     elif request.GET.get('selected_brand'):
#         selected_brand = Brand.objects.get(slug=request.GET.get('selected_brand'))
#         products = Product.objects.filter(brand=selected_brand)

#     else:
#         products = Product.objects.all()
#     categories = Category.objects.all()
#     price_filter = FilterPrice.objects.all()
#     colors = Color.objects.all()
#     brands = Brand.objects.all()
#     if request.GET.get('sortby'):
#         print(products)

#         sortby = request.GET.get('sortby')
#         if sortby=='AtoZ':
#             products = products.order_by('name')
#         elif sortby=='ZtoA':
#             products = products.order_by('-name')
#             print(products)
#         elif sortby=='ascending-price':
#             products = products.order_by('price')
#             print(products)
#         elif sortby=='decending-price':
#             products = products.order_by('-price')

#     context = {'products':products,'categories':categories,'products_count':Product.objects.all().count()}
#     context['price_filter']=price_filter
#     context['colors']=colors
#     context['brands']=brands

#     return render(request,'store/products.html',context)


# def search(request):
#     products = Product.objects.all()
#     search = request.POST.get('search')
#     if request.method == "POST":
#         if search:
#             products = Product.objects.filter(name__icontains=search)
#     context = {'products':products,'search':search}
#     return render(request,'store/search.html',context)


# def product_detail(request,slug):
#     product = Product.objects.filter(slug=slug)
#     print(product,'====================')
#     context = {'product':product.first}
#     return render(request,'store/product_detail.html',context)

# def contact(request):
#     if request.method == 'POST': 
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         contact = Contact.objects.create(name=name,email=email,subject=subject,message=message)
#         contact.save()
#         from django.core.mail import send_mail
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [settings.EMAIL_HOST_USER],
#             fail_silently=False,
#         )
#         return redirect('/')
#     return render(request,'store/contact.html')


# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         first_name = request.POST.get('fname')
#         last_name = request.POST.get('lname')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')
#         if password==cpassword:
#             user = User.objects.create(username=username, email=email)
#             user.first_name = first_name
#             user.last_name = last_name
#             user.set_password(password)
#             user.save()
#             messages.warning(request,"Confirm Password Not Mached")
#     return render(request,'store/login.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(username=username,password=password)
#         if user is not None:
#             auth.login(request,user)

#             wishlist = Wishlist.objects.filter(user=user)
#             request.session['wishlist_count'] = wishlist.count()
#             compares = Compare.objects.filter(user=user)
#             request.session['compare_count'] = compares.count()
#             return redirect('index')
#         else:
#             messages.warning(request,"Invalid Credentials")
#     return render(request,'store/login.html')


# def logout(request):
#     user = request.user
#     if user:
#         auth.logout(request)
#     return redirect('login')



# @login_required(login_url="/login")
# def cart_add(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect("index")


# @login_required(login_url="/login")
# def item_clear(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.remove(product)
#     return redirect("cart_detail")


# @login_required(login_url="/login")
# def item_increment(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect("cart_detail")


# @login_required(login_url="/login")
# def item_decrement(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.decrement(product=product)
#     return redirect("cart_detail")


# @login_required(login_url="/login")
# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect("cart_detail")


# @login_required(login_url="/login")
# def cart_detail(request):
#     return render(request, 'store/cart.html')

# def checkout(request):

 
#     return render(request,'store/checkout.html')

# @login_required(login_url='/login')
# def place_order(request):
#     amount =  int(request.POST.get("amount"))
#     print(amount)
#     data = { "amount":amount*100, "currency": "INR", "receipt": "order_rcptid_11" }
#     payment = client.order.create(data=data)
#     context = {
#         'payment':payment,
#         'key_id':settings.razor_pay_key_id
#     }
#     print(context)

#     first_name = request.POST.get('first_name')
#     last_name = request.POST.get('last_name')
#     country =  request.POST.get('country')
#     address = request.POST.get('address')
#     city = request.POST.get('city')
#     state = request.POST.get('state')
#     postcode = request.POST.get('postcode')
#     phone = request.POST.get('phone')
#     email = request.POST.get('email')
#     additional_info = request.POST.get('additional_info')
#     amount = data.get('amount')
#     order_id =payment['id']
    
#     order = Order.objects.create(
#         user = User.objects.get(pk=request.user.pk),
#         first_name=first_name,
#         last_name=last_name,
#         country=country,
#         address=address,
#         city=city,
#         state=state,
#         postcode=postcode,
#         phone=phone,
#         email=email,
#         additional_info=additional_info,
#         amount=amount,
#         order_id=order_id,
#     )
#     order.save()

#     cart = request.session.get('cart')
#     for item in cart:
#         order_id = OrderItem.objects.create(
#             order = order,
#             product = cart[item]['name'],
#             image = cart[item]['image'],
#             price = cart[item]['price'],
#             total = str(int(cart[item]['price'])*int(cart[item]['quantity'])),
#             quantity = cart[item]['quantity']
#         )
#     print(cart)
#     print('cart')
#     return render(request,'store/place_order.html',context)

# @login_required(login_url='/login')
# def success(request):
#     order_id = request.GET.get('order_id')
#     razorpay_payment_id = request.GET.get('razorpay_payment_id')
#     razorpay_signature = request.GET.get('razorpay_signature')

#     order = Order.objects.get(order_id=order_id)
#     order.razorpay_payment_id = razorpay_payment_id
#     order.razorpay_signature = razorpay_signature
#     order.paid = "True"
#     order.save()
#     cart = Cart(request)
#     cart.clear()
#     return render(request,'store/thank_you.html')

# @login_required(login_url='/login')
# def user_wishlist(request,slug):
#     user = User.objects.get(username=request.user.username)
#     product = Product.objects.get(slug=slug)
#     try:
#         print(product)
#         existing_wishlist = Wishlist.objects.get(user=user,product=product)
#         print(existing_wishlist)
#         existing_wishlist.delete()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     except:
#         wishlist =Wishlist.objects.create(user=user,product=product)
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# @login_required(login_url='/login')
# def view_wishlist(request):
#     wishlists = Wishlist.objects.filter(user=request.user)
#     context = {'wishlists':wishlists}
#     return render(request,'store/wishlist.html',context)

# @login_required(login_url='/login')
# def my_account(request):
#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         birth_date = request.POST.get('birth_date')
#         user = User.objects.get(id=request.user.id)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.email = email
#         user.save()
#         profile = Profile.objects.get(user=user)
#         profile.birth_date = birth_date
#         profile.save()
#     orders = Order.objects.filter(user=request.user)
#     profile = Profile.objects.get(user=request.user)
#     profile.birth_date = profile.birth_date.strftime("%Y-%m-%d")
#     context = {'orders':orders,'profile':profile}
#     return render(request,'account/account.html',context)

# @login_required(login_url='/login')
# def order_detail(request,pk):
#     order_item = OrderItem.objects.get(pk=pk)
#     context = {'order_item':order_item}
#     return render(request,'account/order_detail.html',context)

# @login_required(login_url='/login')
# def add_review(request):
#     user = User.objects.get(username=request.user)
#     product = Product.objects.get(id=request.POST.get('product_id'))
#     message = request.POST.get('message')
#     if message is None:
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
#     review = Review.objects.create(user=user,product=product,message=message)
#     review.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

# @login_required(login_url='/login')
# def compare(request):
#     products = Product.objects.all()
#     compare_products = Compare.objects.filter(user=request.user)
#     context = {'products':products,'compare_products':compare_products}
#     return render(request,'store/compare.html',context)

# @login_required(login_url='/login')
# def add_to_campare(request,slug):
#     user = User.objects.get(username=request.user.username)
#     product = Product.objects.get(slug=slug)
#     try:
#         print(product)
#         existing_compare = Compare.objects.get(user=user,product=product)
#         print(existing_compare)
#         existing_compare.delete()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     except:
#         compare =Compare.objects.create(user=user,product=product)
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         user = User.objects.get(email=email)
#         from_email = user.email
#         global otp
#         request.session['otp'] = random.randint(1000,9999)
#         request.session['email'] = email
#         otp = request.session['otp']
#         send_otp('OTP Verification',f'Your OTP for forgot password is {otp}',from_email,['to@example.com'])
#         return render(request,'account/verify_otp.html')
#     return render(request,'account/forgot_password.html')

# def verify_otp(request):
#     if request.method=='POST':
#         email = request.session.get('email')
#         otp = request.session.get('otp')
#         entered_otp = request.POST['entered_otp']
#         user = User.objects.get(email=email)
#         print(type(otp))
#         print(type(entered_otp),entered_otp != otp)
#         if int(entered_otp) != int(otp):
#             messages.error(request,"Incorrect OTP")
#             return render(request,'account/verify_otp.html')
#         else:
#             context = {'entered_otp':entered_otp}
#             auth.login(request,user)
#             return render(request,'account/change_password.html',context)
#     return render(request,'account/verify_otp.html')


# def change_password(request):
#     if not request.POST.get('entered_otp') or not request.session.get('otp'):
#         return redirect('login')
#     email = request.session.get('email')
#     new_password = request.POST.get('new_password')
#     new_cpassword = request.POST.get('new_cpassword')
#     if new_password==new_cpassword:
#         user = User.objects.get(email=email)
#         user.set_password(new_password)
#         user.save()
#         messages.success(request,'Your Password Has Been Changed')
#         del request.session['otp']
#         del request.session['email']
#         return redirect('login')
#     else:
#         context = {'entered_otp':request.POST.get('entered_otp')}
#         messages.error(request,"Confirm Password Doesn't matched")
#         return render(request,'account/change_password.html',context)


# def fetch_resources(url,rel):
#     path = os.path.join(ur)