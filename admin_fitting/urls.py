from django.urls import path,include
from rest_framework_simplejwt.views import  TokenRefreshView 
from .views import AdminFittingViewSet
from .views import CustomTokenObtainPairView
from rest_framework.routers import DefaultRouter
from consumer.views import ProfileViewSet
from .views import GettingStartedInfoDetailView
from consumer.views import UserProfileUpdateView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
# router.register(r'fittings', AdminFittingViewSet, basename='fittings')

urlpatterns = [
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('fittings', AdminFittingViewSet.as_view({'get': 'list'}), name='fitting-list'),
    path('fittings/<int:pk>', AdminFittingViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='fitting-detail'),
    path('getting-started-info', GettingStartedInfoDetailView.as_view(), name='getting-started-info'),
    path('user/profile/<int:pk>', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('', include(router.urls)),
]
