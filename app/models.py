from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class products_category(models.Model):
    id=models.AutoField(primary_key=True)
    category=models.CharField(max_length=100)
   
    def __str__(self):
        return self.category

class product_details(models.Model):
    id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    product_price=models.CharField(max_length=50)
    # product_image=models.URLField(max_length=10000)
    product_image=models.ImageField(upload_to='image/')
    product_category=models.ForeignKey(products_category,on_delete=models.CASCADE)
   

    def __str__(self):
        return self.product_name