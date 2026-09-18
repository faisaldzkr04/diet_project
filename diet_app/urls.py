from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('user/', views.user_page, name='user_page'),
    path('dietadmin/', views.admin_page, name='admin_page'),  # Ubah di sini
    path('dietadmin/add_food/', views.add_food_page, name='add_food_page'),
    path('dietadmin/update_food/<int:pk>/', views.update_food_page, name='update_food_page'),
    path('dietadmin/delete_food/<int:pk>/', views.delete_food, name='delete_food'),

    # Login & Logout
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)