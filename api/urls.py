from django.urls import include, path

from api.viewsets.auth import CustomTokenObtainPairView, CustomTokenRefreshView, UserRegisterView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework import routers

from api.viewsets.product import DepartmentViewSet, VariantNameViewSet, VariantViewSet, VariantsReportView
from api.viewsets.users import LoggedInUserProfile, UserViewSet

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users-views") 
router.register("departments", DepartmentViewSet, basename="dept-views")
router.register("variant-names", VariantNameViewSet, basename="variant-name-views")
router.register("variants", VariantViewSet, basename="variants-views")


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
    path("variant/report", VariantsReportView.as_view()),
    path("", include(router.urls)),
]

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)

