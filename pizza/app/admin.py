from django.contrib import admin
from app.models import *
# Register your models here.
admin.site.register(PizaaCategory)
admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Coupon)