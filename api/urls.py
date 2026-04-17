from django.urls import include, path

from api.viewsets.auth import CustomTokenObtainPairView, CustomTokenRefreshView, UserRegisterView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework import routers

from api.viewsets.logged_in_users import  UserCartListAction, CouponApplyView
from api.viewsets.product import DepartmentViewSet, VariantNameViewSet, VariantViewSet,ProductViewSet, CouponCodeViewSet
from api.viewsets.users import LoggedInUserProfile, UserViewSet

from api.viewsets.public import DepartmentView,VariantsView, ProductsView


router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users-views") 
router.register("departments", DepartmentViewSet, basename="dept-views")
router.register("variant-names", VariantNameViewSet, basename="variant-name-views")
router.register("variants", VariantViewSet, basename="variants-views")
router.register("products", ProductViewSet, basename="product-views")
router.register("coupon", CouponCodeViewSet, basename="coupon-codes-views")


urlpatterns = [
    # SWAGGER URLS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # SWAGGER URLS
    path("auth/", include([
        path("register/", UserRegisterView.as_view()),

        path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
        # 
        path("get-my-profile/", LoggedInUserProfile.as_view()),
    ])),

    path('public/', include([
        path('departments/', DepartmentView.as_view()),
        path('variants/', VariantsView.as_view()),
        path('products/', ProductsView.as_view()),
        # LOGGED IN USER APIs
        path('cart/', UserCartListAction.as_view()),
        path('apply-coupon/', CouponApplyView.as_view()),

    ])),

    path("", include(router.urls)),
]

