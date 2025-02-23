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
    ('FN','Furniture'),
    ('SO','Sofas/Seating'),
    ('KD','Kitchen/Dining'),
    ('LB','Living/Bedroom'),
    ('OL','Outdoor Living'),
    ('HD','Home Decor'),
    ('HA','Home Appliances'),
    ('EL','Electronics'),
    ('LL','Lamps/Lighting'),
    ('TV','TV/Audio/vedio'),
    ('AS','Air Solutions'),
    ('CM','Computing/Mobile'),
    ('OF','Office furniture'),
    ('SP','Stool&Pouffes'),
    ('SF','Sofas'),
    ('CH','Chairs'),
    ('TB','Tables'),
    ('WD','Wardrobes'),
    ('BE','Beds'),
    ('SR','Shoe Racks'),
    ('CS','Cabinets & Sideboards'),
    ('SS','Sectional Sofas'),
    ('RC','Recliners'),
    ('BS','Book Shelves'),
    ('OT','Ottomans'),


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
    PAYMENT_CHOICES = [
        ("credit_card", "Credit Card"),
        ("paypal", "PayPal"),
        ("cod", "Cash on Delivery"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cod")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")  # Fix Here
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
