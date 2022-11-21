from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:message_id>/', views.get_message, name='get_message'),
    path("register/", views.register, name="register")
]
