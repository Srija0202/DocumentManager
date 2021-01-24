from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('document/', document, name='document'),
    path('document/add/', document_add, name='document_add'),
    path('document/<int:id>/', document_edit, name='document_edit'),
    path('document/delete/<int:id>/', document_delete, name='document_delete'),
]