from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('items', views.CartItemViewSet, basename='cart-items')
router.register('', views.CartView, basename='cart')

urlpatterns = router.urls