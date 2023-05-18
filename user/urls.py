from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views

app_name = "user"

urlpatterns = [
    path('login/', views.UserLoginAPI.as_view(), name='login'),
    path('token/',  views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
