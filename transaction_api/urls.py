from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.transactions_manager),
    path('transactions/<int:id>/', views.transaction_specific_manager),
    path('summary/', views.transactions_summary)
]
