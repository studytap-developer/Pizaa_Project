from django.shortcuts import render,redirect
from app.models import *
# from locust import User
from django.contrib import messages
from django.contrib.auth.models import User# Create your views here.
from django.contrib.auth import login,authenticate,logout
from instamojo_wrapper import Instamojo
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image, Paragraph
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView


print("After class definition")
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN,endpoint="https://test.instamojo.com/api/1.1/")



def index(request):
    pizza_list=Pizza.objects.all()
    context={"pizza_list":pizza_list}

    return render(request,"app/index.html",context)


def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user_obj, created = User.objects.get_or_create(username=username)
            
            if not created:
                messages.error(request, "Username already exists")
                return redirect("/register/")

            user_obj.set_password(password)  # Hash the password
            user_obj.save()

            messages.success(request, "Account created successfully")
            return redirect("/login")
        except Exception as e:
            messages.error(request, "Something went wrong: " + str(e))
            return redirect("/register")

    return render(request, "app/register.html")


def login_page(request):
    if request.method=="POST":

        try:
            username=request.POST.get("username")
            password=request.POST.get("password")
            user_obj=User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, "UserName not found")
                return redirect("/login/")
            user_obj=authenticate(username=username,password=password)
            if user_obj:
                login(request,user_obj)
                return redirect("/")
            messages.success(request, "wrong password")
            return redirect("/login")
        except Exception as e:
            messages.error(request, "Something went wrong")
    return render(request,"app/login.html")


def logout_view(request):
    logout(request)
    return redirect('/login')

def add_cart(request,pizza_uid):
    user=request.user
    pizza_obj=Pizza.objects.get(uid=pizza_uid)
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
    cart_items=CartItems.objects.create(
        cart=cart,
        pizaa=pizza_obj
    )
    return redirect("/")
    # return render(request,"app/add_cart.html")


def cart(request):
    try:
        carts=Cart.objects.get(is_paid=False,user=request.user)
        cart_items = carts.cart_items.all()
        if not cart_items.exists():  # Check if the cart is empty
            messages.info(request, "Your cart is empty.")
            return render(request, "app/empty_cart.html")  # Redirect to the empty cart template


        response=api.payment_request_create(
            amount= carts.get_cart_total(),
            purpose="Order",
            buyer_name=request.user.username,
            email="studytapdevloper@gmail.com",
            redirect_url="http://127.0.0.1:8000/success/"

        )
        carts.instamojo_id=response["payment_request"]["id"]
        carts.save()
        context={"carts":carts,"payment_url":response["payment_request"]["longurl"]}
        print(response)
        return render(request,"app/cart.html",context)
    except Cart.DoesNotExist:
        # Handle the case where the cart does not exist
        # For instance, show a message or redirect to a page
        messages.info(request, "Your cart is empty.")
        return render(request, "app/empty_cart.html")  # Redirect to an appropriate template
def remove_cart_items(request,cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()
        return redirect("/cart")
    except Exception as e:
        print(e)


def orders(request):
    orders=Cart.objects.filter(is_paid=True,user=request.user).order_by("-created_at")
    context={"orders":orders}
    return render(request,"app/oder.html",context)


def success(request):
    payment_request=request.GET.get("payment_request_id")
    cart=Cart.objects.get(instamojo_id=payment_request)
    cart.is_paid=True
    cart.save()
    return redirect("/orders")






from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.units import inch

def generate_invoice(request, order_id):
    try:
        order = Cart.objects.get(uid=order_id, user=request.user, is_paid=True)
        cart_items = order.cart_items.all()
        user_details = order.user

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Add Company Logo
        # logo_path = settings.COMPANY_LOGO_PATH
        # logo = Image(logo_path, width=2*inch, height=1*inch)
        # story.append(logo)

        # Company Details
        story.append(Spacer(1, 12))
        story.append(Paragraph("Company Name", styles["Normal"]))
        story.append(Paragraph(f"GST No: {settings.COMPANY_GST_NO}", styles["Normal"]))

        # User Details
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"USERNAME: {user_details.username}", styles["Normal"]))
        story.append(Paragraph(f"Email: {user_details.email}", styles["Normal"]))
        # story.append(Paragraph(f"Phone: {user_details.phone_number}", styles["Normal"]))
        # story.append(Paragraph(f"Address: {order.order_address}", styles["Normal"]))

        # Invoice Items Table
        data = [["Item", "Price"]]
        for item in cart_items:
            data.append([item.pizaa.pizza_name, f"{item.pizaa.price}"])

        if order.coupon:
            data.append(["Discount", f"{order.coupon.discount_price}"])

        data.append(["Total", f"{order.get_cart_total()}"])
        table = Table(data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ]))
        story.append(table)

        doc.build(story)
        return response
    except Cart.DoesNotExist:
        return HttpResponse("Order not found", status=404)


