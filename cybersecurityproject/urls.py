from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView

from .views import redirect
urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),  
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='insecureApp/login.html')),
    path('messages/', include('insecureApp.urls')),
    path('', redirect)
]
