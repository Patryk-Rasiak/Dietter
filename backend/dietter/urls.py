from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dietter_auth.urls')),
    path('user/', include('users.urls')),
    path('meals/', include('meals.urls')),
    path('diets/', include('diets.urls')),
    path('ratings/', include('ratings.urls')),
]
