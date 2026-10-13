from django.urls import path
from application.views import (
    addToCartView, decreaseCartItemView, indexView, medicinesListView, cartView, checkoutView, confirmationView,
    companyListView, addCompanyView, customerRequestListView, addCustomerRequestView,
    dashboardView, loginView, logoutView, movie_recommendation_view, movie_result, removeFromCartView, signupView
)
# For Medicines list and cart operations (add, remove, decrease)
# For Checkout and order confirmation
#  For Company management (list and add)
#  For Customer medicine requests (view and add)
#  For User authentication (login, logout, signup)
#  For Admin dashboard view
# For Fun feature: Movie recommendation via external API
urlpatterns = [
    path('', indexView, name='home'),
    path('medicines/', medicinesListView, name='medicines_list'),
    path('cart/', cartView, name='cart'),
    path('checkout/', checkoutView, name='checkout'),
    path('order-confirmation/', confirmationView, name='order_confirmation'),
    path('companies/', companyListView, name='companyList'),
    path('companies/add/', addCompanyView, name='addCompany'),
    path('customer-requests/', customerRequestListView, name='customer_request_list'),
    path('customer-requests/add/', addCustomerRequestView, name='addCustomerRequest'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('signup/', signupView, name='signup'),
    path('cart/add/<int:medicine_id>/', addToCartView, name='add_to_cart'),
    path('cart/decrease/<int:item_id>/', decreaseCartItemView, name='decrease_cart_item'),
    path('cart/remove/<int:item_id>/', removeFromCartView, name='remove_from_cart'),
    path('movie-recommendation/', movie_recommendation_view, name='movierecommendation'),
    path('movie-result/', movie_result, name='movieresult'),
]
