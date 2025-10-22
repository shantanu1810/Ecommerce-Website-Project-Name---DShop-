from django.db import models
import datetime
import os


# Models Created 
class Customers(models.Model):
    username=models.TextField(max_length=40)
    email=models.TextField(max_length=40)
    password=models.TextField(max_length=16)
    Address=models.TextField(max_length=100,null=True)
    phone_no=models.TextField(max_length=10,null=True)
    customer_name=models.TextField(max_length=50,null=True)
    cart=models.JSONField(default=list,blank=True)
    order=models.JSONField(default=list,blank=True)
    alternate_no=models.TextField(max_length=10,null=True)
    alternate_email=models.TextField(max_length=40,null=True)
    gifts=models.JSONField(default=list,blank=True)
    


class Bussiness(models.Model):
    bussiness_name=models.TextField(max_length=40)
    bussiness_email=models.TextField(max_length=40)
    password=models.TextField(max_length=16)
    Address=models.TextField(max_length=100,null=True,default="")
    phone_no=models.TextField(max_length=10,null=True,default="")
    owner_name=models.TextField(max_length=50,null=True,default="")
    products=models.JSONField(default=list,blank=True)
    no_of_products=models.TextField(max_length=20,null=True)


#DShop.Products.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
# HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".
def filepath(request,filename):
    old_filename=filename
    timenow=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename="%s%s",(timenow,old_filename)
    return os.path.join('upload/',filename)


class Products(models.Model):
    product_id=models.TextField(max_length=15,null=True)
    name=models.TextField(max_length=200)
    price=models.TextField(max_length=40)
    description=models.TextField(max_length=500, null=True)
    image=models.ImageField(upload_to='upload/',null=True,blank=True)
    product_type=models.TextField(max_length=50,null=True)
    brand=models.TextField(max_length=30,null=True)
    sub_type=models.TextField(max_length=50,null=True)
    discount=models.TextField(max_length=4,null=True,default="0")
    order_quantity=models.JSONField(default=dict,blank=True)
    average_rating=models.TextField(max_length=4,null=True)
    people_buy=models.TextField(max_length=10,default="0")
    people_rate=models.TextField(max_length=10,default="0")
    new_order=models.TextField(max_length=3,default="0")
    feedback_rating=models.JSONField(default=list,blank=True)
    ratings=models.JSONField(default=list,blank=True)

class Offer_Gifts(models.Model):
    OfferID=models.TextField(max_length=20,null=True)
    name=models.TextField(max_length=50,null=True)
    details=models.TextField(max_length=200,null=True)
    discount_amount=models.TextField(max_length=10,null=True)
    condition=models.TextField(max_length=50,null=True)
