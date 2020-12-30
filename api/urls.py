from django.urls import include, path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]