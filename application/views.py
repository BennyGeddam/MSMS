# application/views.py

from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from application.models import Company, CompanyBank, CustomerRequest, Medicine, Order, OrderItem
from django.shortcuts import get_object_or_404, redirect
from application.models import Cart, CartItem, Medicine
from django.contrib.auth.decorators import login_required
from application.forms import CustomerRequestForm
from django.contrib.auth.forms import UserCreationForm

def indexView(request):
    return render(request, 'application/index.html')

@login_required
def companyListView(request):
    companies = Company.objects.all()
    return render(request, 'application/company_list.html', {'companies': companies})


@login_required
def addCompanyView(request):
    return render(request, 'application/add_company.html')


@login_required
def medicinesListView(request):
    medicines = Medicine.objects.all()
    return render(request, 'application/medicines_list.html', {'medicines': medicines})


@login_required
def cartView(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    medicine_id = request.GET.get('add')
    if medicine_id:
        medicine = get_object_or_404(Medicine, id=medicine_id)

        item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)
        if not created:
            item.quantity += 1
            item.save()
        return redirect('cart')


    cart_items = cart.items.select_related('medicine').all()
    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'application/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


class DummyCheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    phone = forms.CharField(max_length=15)

@login_required
def checkoutView(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('medicine').all()

    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        form = DummyCheckoutForm(request.POST)
        if form.is_valid():
            # Save the order
            order = Order.objects.create(user=request.user, total_price=total_price)
            for item in cart_items:
                OrderItem.objects.create(order=order, medicine=item.medicine, quantity=item.quantity)

            # Clear the cart
            cart.items.all().delete()

            messages.success(request, "Order placed successfully!")
            return redirect('order_confirmation')
    else:
        form = DummyCheckoutForm()

    return render(request, 'application/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def confirmationView(request):
    return render(request, 'application/confirmation.html')


@login_required
def customerRequestListView(request):
    customer_requests = CustomerRequest.objects.all()

    if request.method == 'POST':
        form = CustomerRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your request was submitted.")
            return redirect('customer_request_list')
    else:
        form = CustomerRequestForm()

    return render(request, 'application/customerrequestlist.html', {
        'form': form,
        'customer_requests': customer_requests
    })


@login_required
def dashboardView(request):
    if not request.user.is_staff:
        raise PermissionDenied("You are not authorized to view this page.")

    customer_requests = CustomerRequest.objects.all()
    company_banks = CompanyBank.objects.select_related('company').all()

    return render(request, 'application/dashboard.html', {
        'customer_requests': customer_requests,
        'company_banks': company_banks,
    })


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'application/login.html')


def logoutView(request):
    logout(request)
    return redirect('login')


def signupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'application/signup.html', {'form': form})


@login_required
def addToCartView(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def removeFromCartView(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def addCustomerRequestView(request):
    if request.method == 'POST':
        form = CustomerRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_request_list')
    else:
        form = CustomerRequestForm()
    return render(request, 'application/addcustomerrequest.html', {'form': form})

@login_required
def decreaseCartItemView(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:

        cart_item.delete()

    return redirect('cart')
from django.http import JsonResponse
import requests

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests

@login_required
def movie_recommendation_view(request):
    return render(request, 'application/movierecommendation.html')

@login_required
def movie_result(request):
    mood = request.GET.get("mood", "").strip()
    time_of_day = request.GET.get("time_of_day", "").strip()
    watching_with = request.GET.get("watching_with", "").strip()

    if not mood or not time_of_day or not watching_with:
        return redirect("movierecommendation")

    MOVIE_API_URL = "https://bqi07udsdd.execute-api.eu-west-1.amazonaws.com/recommend"
    payload = {
        "mood": mood,
        "time_of_day": time_of_day,
        "watching_with": watching_with
    }

    try:
        response = requests.post(MOVIE_API_URL, json=payload)
        movie_data = response.json()

        if not movie_data or "error" in movie_data or not movie_data.get("title"):
            movie_data = {
                "title": "No Recommendation Found",
                "genre": "N/A",
                "summary": "No movies matched your criteria. Try again with different options."
            }

    except requests.RequestException as e:
        movie_data = {
            "title": "Error",
            "genre": "N/A",
            "summary": f"Failed to fetch movie. Error: {str(e)}"
        }

    return render(request, 'application/movieresult.html', {"movie": movie_data})
