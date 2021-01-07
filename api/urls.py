from django.urls import include, path
from . import views

urlpatterns = [
    path('users/<str:uid>/', views.UserView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('products/<int:uid>/', views.ProductView.as_view()),
    path('cart/<int:uid>/', views.CartView.as_view()),
    path('add-to-cart/', views.AddToCart.as_view()),
    path('delete-from-cart/<int:uid>/<int:cartId>/<int:userId>/', views.DeleteFromCart.as_view()),
    path('decrease-from-cart/<int:uid>/<int:cartId>/<int:userId>/', views.DecreaseFromCart.as_view()),
    path('category/', views.GetCategory.as_view()),
    path('getuserid/', views.UserId.as_view(), name='Getuserview'),
    path('get-cart-products/', views.CartProducts.as_view())
]