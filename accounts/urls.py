
from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signUp, name='Sign Up'),
    path("member_auth", views.memberPass, name='Member Authentication')
]
