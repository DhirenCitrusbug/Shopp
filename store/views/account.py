from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from ..models import Compare, Order, Product, Contact, Profile, Review, Wishlist
from shop import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from shop import settings
import random
from ..task import send_otp

# Create your views here.


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

            wishlist = Wishlist.objects.filter(user=user)
            request.session['wishlist_count'] = wishlist.count()
            compares = Compare.objects.filter(user=user)
            request.session['compare_count'] = compares.count()
            return redirect('index')
        else:
            messages.warning(request,"Invalid Credentials")
    return render(request,'store/login.html')


def logout(request):
    user = request.user
    if user:
        auth.logout(request)
    return redirect('login')

@login_required(login_url='/login')
def my_account(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        profile = Profile.objects.get(user=user)
        profile.birth_date = birth_date
        profile.save()
    orders = Order.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    profile.birth_date = profile.birth_date.strftime("%Y-%m-%d")
    context = {'orders':orders,'profile':profile}
    return render(request,'account/account.html',context)


@login_required(login_url='/login')
def add_review(request):
    user = User.objects.get(username=request.user)
    product = Product.objects.get(id=request.POST.get('product_id'))
    message = request.POST.get('message')
    if message is None:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    review = Review.objects.create(user=user,product=product,message=message)
    review.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

@login_required(login_url='/login')
def compare(request):
    products = Product.objects.all()
    compare_products = Compare.objects.filter(user=request.user)
    context = {'products':products,'compare_products':compare_products}
    return render(request,'store/compare.html',context)

@login_required(login_url='/login')
def add_to_campare(request,slug):
    user = User.objects.get(username=request.user.username)
    product = Product.objects.get(slug=slug)
    try:
        print(product)
        existing_compare = Compare.objects.get(user=user,product=product)
        print(existing_compare)
        existing_compare.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        compare =Compare.objects.create(user=user,product=product)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(email=email)
        from_email = user.email
        global otp
        request.session['otp'] = random.randint(1000,9999)
        request.session['email'] = email
        otp = request.session['otp']
        send_otp('OTP Verification',f'Your OTP for forgot password is {otp}',from_email,['to@example.com'])
        return render(request,'account/verify_otp.html')
    return render(request,'account/forgot_password.html')

def verify_otp(request):
    if request.method=='POST':
        email = request.session.get('email')
        otp = request.session.get('otp')
        entered_otp = request.POST['entered_otp']
        user = User.objects.get(email=email)
        print(type(otp))
        print(type(entered_otp),entered_otp != otp)
        if int(entered_otp) != int(otp):
            messages.error(request,"Incorrect OTP")
            return render(request,'account/verify_otp.html')
        else:
            context = {'entered_otp':entered_otp}
            auth.login(request,user)
            return render(request,'account/change_password.html',context)
    return render(request,'account/verify_otp.html')


def change_password(request):
    if not request.POST.get('entered_otp') or not request.session.get('otp'):
        return redirect('login')
    email = request.session.get('email')
    new_password = request.POST.get('new_password')
    new_cpassword = request.POST.get('new_cpassword')
    if new_password==new_cpassword:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        messages.success(request,'Your Password Has Been Changed')
        del request.session['otp']
        del request.session['email']
        return redirect('login')
    else:
        context = {'entered_otp':request.POST.get('entered_otp')}
        messages.error(request,"Confirm Password Doesn't matched")
        return render(request,'account/change_password.html',context)



