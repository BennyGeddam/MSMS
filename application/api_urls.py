from django.urls import include, path
from rest_framework.routers import DefaultRouter
from application.api_views import (
    CompanyViewSet,
    MedicineViewSet,
    CompanyBankViewSet,
    CustomerRequestViewSet,
)
# routing for API endpoints using Django REST Framework.
#    companies:          CompanyViewSet
#    medicines:          MedicineViewSet
#    company-banks:      CompanyBankViewSet
#    customer-requests:  CustomerRequestViewSet
router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'company-banks', CompanyBankViewSet)
router.register(r'customer-requests', CustomerRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
