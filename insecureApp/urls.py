from django.urls import path
from . import views

app_name = 'insecureApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:message_id>/', views.get_message, name='get_message'),
    path("register/", views.register, name="register"),
    # Swap out line 10, use line 11 for safe database access.
    path('injection_post/', views.post_injection_message, name="injection_post")
    #path('injection_post/', views.post_safe_message, name="injection_post") 
    
]
