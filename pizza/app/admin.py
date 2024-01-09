from django.contrib import admin
from django.db.models import Sum
from .models import *
# Register your models here.
# admin.site.register(PizaaCategory)
# admin.site.register(Pizza)
# admin.site.register(Cart)
# admin.site.register(CartItems)
# admin.site.register(Coupon)
class CartItemsInline(admin.TabularInline):
    model = CartItems
    extra = 0
@admin.register(PizaaCategory)
class PizaaCategoryAdmin(admin.ModelAdmin):
    list_display=["category_name"]
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display=["pizza_name","price","image"]
from django.contrib import admin
from django.db.models import Sum
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["__str__","status", "is_paid", "instamojo_id", "order_date", "delivered_date", "get_cart_total"]
    list_editable = ["status"]
    list_filter = ["status"]
    search_fields = ["user__username", "user__email", "instamojo_id"]
    inlines = [CartItemsInline]

    def user_username(self, obj):
        return obj.user.username if obj.user else None

    user_username.short_description = 'User'

    def email(self, obj):
        return obj.user.email if obj.user else None

    email.short_description = 'Email'

    def get_cart_total(self, obj):
        return obj.get_cart_total()

    get_cart_total.short_description = 'Total'

    def instamojo_id_display(self, obj):
        return obj.instamojo_id[:10] + "..." if obj.instamojo_id else None

    instamojo_id_display.short_description = 'Instamojo ID'

    def cart_items_count(self, obj):
        return obj.cartitems_set.count()

    cart_items_count.short_description = 'Cart Items'

    readonly_fields = ('user_username', 'email', 'get_cart_total', 'instamojo_id_display', 'cart_items_count', 'order_date', 'delivered_date')

    def get_queryset(self, request):
        return super().get_queryset(request)

    ordering = ['-order_date']  # Assuming 'order_date' is the correct field for ordering

    def save_model(self, request, obj, form, change):
        # Override the save_model method to set order_date and delivered_date, and save the model immediately
        obj.order_date = obj.order_date or timezone.now()

        # If the status is set to "Delivered," update the delivered_date
        if obj.status == Cart.DELIVERED:
            obj.delivered_date = timezone.now()

        obj.save()

@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ["cart", "pizaa_name", "price", "created_at"]

    def pizaa_name(self, obj):
        return obj.pizaa.pizza_name if obj.pizaa else None

    pizaa_name.short_description = 'Pizza Name'

    def price(self, obj):
        return obj.pizaa.price if obj.pizaa else None

    price.short_description = 'Pizza Price'