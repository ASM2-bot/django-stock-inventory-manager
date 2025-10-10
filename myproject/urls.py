# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # This includes built-in auth views
    path('', include('main.urls',namespace='main')),  # Include your 'main' app's URLs

]
