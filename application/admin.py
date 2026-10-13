from django.contrib import admin
from .models import (
    Company,
    CompanyBank,
    Medicine,
    CustomerRequest,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


admin.site.register(Company)
admin.site.register(CompanyBank)
admin.site.register(Medicine)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'medicine_details', 'status')
    search_fields = ('customer_name', 'phone')
    list_filter = ('status',)
