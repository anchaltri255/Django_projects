from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATE_CHOICES = (
    ('Delhi','Delhi'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Gujrat', 'Gujrat'),
    ('Bihar','Bihar'),
    ('Assam','Assam'),
    ('Haryana','Haryana'),
    
)

CATEGORY_CHOICES=(
    ('CH','Chair'),
    ('CO','Cooler'),
    ('TB','Table'),
    ('FG','Refrigerator'),
    ('DR','Dressing'),
    ('FUN','Furniture'),
    ('BED','Bed'),
    ('FAN','Ceiling Fan'),
    ('AC','Air Conditioner'),
    ('PR','Press'),
    ('MX','Mixer'),
    ('IN','Induction'),
    ('GZ','Gizar'),
    ('TV','Telivison'),
    ('SF','Sofa'),
    ('WM','Washing Machine'),
)

class Product(models.Model):
    tittle = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.tittle
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()