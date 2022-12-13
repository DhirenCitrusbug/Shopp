from django.db import models
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

class Brand(models.Model):
    name = models.CharField(max_length=100)

class Color(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

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

class Product(models.Model):
    CONDITION = ('New','New'),('Old','Old')
    STOKE = ('In Stock','In Stock'),('Out of Stock','Out of Stock')
    STATUS = ('Publish','Publish'),('Draft','Draft')

    unique_id = models.CharField(max_length=100, unique=True, null=False,blank=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    condition = models.CharField(max_length=100, choices=CONDITION)
    information = models.TextField()
    description = models.TextField()
    stock = models.CharField(max_length=100, choices=STOKE)
    status = models.CharField(max_length=100, choices=STATUS)
    created_date = models.DateTimeField(auto_created=True, default=timezone.now())
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(FilterPrice, on_delete=models.CASCADE)


    def save(self,*args,**kwags):
        if self.unique_id == None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('%Y%m%d') + str(self.id)
        return super().save(*args,**kwags)

class Image(models.Model):
    image = models.ImageField(upload_to='Product_images/img')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    