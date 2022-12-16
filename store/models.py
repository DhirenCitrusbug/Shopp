from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

class Color(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Color, self).save(*args, **kwargs)

class FilterPrice(models.Model):
    FILTER_PRICE = (
        ('1000 TO 10000' ,'1000 TO 10000'),
        ('10000 TO 20000' ,'10000 TO 20000'),
        ('20000 TO 30000' ,'20000 TO 30000'),
        ('30000 TO 40000' ,'30000 TO 40000'),
        ('40000 TO 50000' ,'40000 TO 50000'),
        ('50000 TO 60000' ,'50000 TO 60000'),
        ('60000 TO 70000' ,'60000 TO 70000'),
        ('70000 TO 80000' ,'70000 TO 80000'),
        ('80000 TO 90000' ,'80000 TO 90000'),
        ('90000 TO 100000' ,'90000 TO 100000'),
        ('Above 100000 ',' Above 100000'),

    )

    price = models.CharField(max_length=100,choices=FILTER_PRICE)
    slug = models.SlugField(unique=True,null=True,blank=True)
    def __str__(self):
        return self.price
    def save(self, *args, **kwargs):
        self.slug = slugify(self.price)
        super(FilterPrice, self).save(*args, **kwargs)
        
class Product(models.Model):
    CONDITION = ('New','New'),('Renewed','Renewed'),('Old','Old')
    STOKE = ('In Stock','In Stock'),('Out of Stock','Out of Stock')
    STATUS = ('Publish','Publish'),('Draft','Draft')

    # unique_id = models.CharField(max_length=100, unique=True, null=False,blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True,max_length=200)
    price = models.IntegerField()
    condition = models.CharField(max_length=100, choices=CONDITION)
    information = RichTextField()
    description = RichTextField()
    stock = models.CharField(max_length=100, choices=STOKE)
    status = models.CharField(max_length=100, choices=STATUS)
    created_date = models.DateTimeField(auto_created=True, default=timezone.now())
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name='products')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(FilterPrice, on_delete=models.CASCADE,related_name='products')
    image = models.ImageField(upload_to='products/',default='static/images/product-image/1.webp')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        images = Image.objects.filter(product=self)
        print(images)
        self.image = images[0].image
        super(Product, self).save(*args, **kwargs)

class Image(models.Model):
    image = models.ImageField(upload_to='Product_images/img')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')

class Tag(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='tags')

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.email

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    additional_info = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    paid = models.BooleanField(default=False,null=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self) -> str:
        return self.user.email

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Product_Images/Order_Img")
    quantity = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    total = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.product

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlist')