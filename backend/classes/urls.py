from django.urls import path
from . import views

urlpatterns = [
    path('create_class/', views.create_class, name='create_class'),
    path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),
    path('requesttojoin/<int:class_id>/', views.request_to_join_class, name='requesttojoin'),
    path('joinrequest/<int:membership_id>/', views.handle_join_request, name='joinrequest'),
    path('remove_student/<int:class_id>/<int:student_id>/', views.remove_student, name='remove_student'),
]
