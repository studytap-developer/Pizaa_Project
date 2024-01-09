from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
from django.utils import timezone

# Create your models here.
class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    created_at=models.DateField(auto_now_add=True)
    update_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract=True

class PizaaCategory(BaseModel):
    category_name=models.CharField(max_length=100)

class Pizza(BaseModel):
    category=models.ForeignKey(PizaaCategory,on_delete=models.CASCADE,related_name="pizzas")
    pizza_name=models.CharField(max_length=100)
    price=models.IntegerField(default=100)
    image=models.ImageField(upload_to="pizza")
class Coupon(BaseModel):
    coupon_code=models.CharField(max_length=100)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=50)
    minimun_ammount=models.IntegerField(default=300)

class Cart(BaseModel):
    ORDER_PLACED = 'placed'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'

    ORDER_STATUS_CHOICES = [
        (ORDER_PLACED, 'Order Placed'),
        (IN_TRANSIT, 'In Transit'),
        (DELIVERED, 'Delivered'),
    ]


    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name="carts")
    is_paid=models.BooleanField(default=False)
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=ORDER_PLACED)
    instamojo_id = models.CharField(max_length=100)  
    order_date = models.DateTimeField(default=timezone.now)  # New field for order date
    delivered_date = models.DateTimeField(null=True, blank=True)  # New field for delivered date
    def get_cart_total(self):
        return CartItems.objects.filter(cart =self).aggregate(total_price=Sum("pizaa__price")).get('total_price') or 0
    class Meta:
        ordering = ['-order_date']
    def __str__(self):
        return f"Cart {self.uid} - User: {self.user.username if self.user else 'None'}"
 
class CartItems(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    pizaa=models.ForeignKey(Pizza,on_delete=models.CASCADE)





