from django.urls import path
from .views import AdminProductListCreateView, AdminProductDetailView

urlpatterns = [
    path('', AdminProductListCreateView.as_view(), name='admin-product-list-create'),
    path('<uuid:pk>/',AdminProductDetailView.as_view(), name='admin-product-detail'),
]