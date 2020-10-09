from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from myapp.views import profile_image, success

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'myapp/', include('myapp.urls', namespace='myapp')),
    #path(r'myapp/login/', auth_views.LoginView.as_view()),
    path('', include('django.contrib.auth.urls')),
    #path(r'image_upload/', profile_image, name='image_upload'),
    #path(r'success/', success, name = 'success')

 ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

