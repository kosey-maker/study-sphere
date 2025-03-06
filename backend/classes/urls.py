from django.urls import path
from . import views

urlpatterns = [
    path('create_class/', views.create_class, name='create_class'),
    path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),
    path('remove_student/<int:class_id>/<int:student_id>/', views.remove_student, name='remove_student'),
    path('get_class/<int:class_id>/', views.get_class, name='get_class'),
]
