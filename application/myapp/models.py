from django.db import models

# Create your models here.

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
