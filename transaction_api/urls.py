from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.transactions_manager, name='create_list'),
    path('transactions/<int:id>/', views.transaction_specific_manager, name='retrieve_update_delete'),
    path('summary/', views.transactions_summary, name='summary')
]
