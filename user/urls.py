from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views
from user.views import MyTokenObtainPairView

app_name = "user"

urlpatterns = [
    path('token/',  MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
