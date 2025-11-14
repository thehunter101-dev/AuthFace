from django.db import router
from django.urls import include, path
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.routers import DefaultRouter
from .views import BiometriaViewSet, ProtectedView, BionmetriaView, UserInfo, BiometriacheckView, UserViewSet

router = DefaultRouter()
router.register(r'users',UserViewSet,basename='user')
router.register(r"biometria",BiometriaViewSet,basename="biometria")

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),name='token_optain_pair'),
    path('token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('protected/',ProtectedView.as_view(),name="protected"),
    path('user/info',UserInfo.as_view(),name="user_info"),
    path('img/post', BionmetriaView.as_view(), name="img_post"),
    path('verify-bio/',BiometriacheckView.as_view(),name="verify_bio"),
    path('',include(router.urls))
]