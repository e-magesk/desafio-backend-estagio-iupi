from django.urls import path

from . import views

urlpatterns = [
    path('', views.transactions_manager, name='create_list'),
    path('<int:id>/', views.transaction_specific_manager, name='retrieve_update_delete')
]
