from django.urls import path
from .views import tasks
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register),
    path('tasks/', tasks),
    path('tasks/<int:id>', tasks),
    path('test/', views.test),
    path('send/', views.send),
    path('get_all_images', views.getTasks),
    path('upload_image/', views.ImageUpload.as_view()),
    path('mymodel/', views.MyModelView.as_view()),
    path('mymodel/<int:pk>/', views.MyModelView.as_view()),
    path('mprint/', views.MPrintView.as_view()),
    path('mprint/<int:pk>/', views.MPrintView.as_view()),

    # upload images
]
# data - OK
# authentication - OK
# upload files (image)
