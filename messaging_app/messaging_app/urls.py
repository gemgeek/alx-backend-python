from django.contrib import admin  # type: ignore
# Make sure 'include' is imported
from django.urls import path, include  # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
]
