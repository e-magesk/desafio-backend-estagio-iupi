from django.urls import path

from . import views

urlpatterns = [
    path('', views.transactions_manager),
    path('<int:id>/', views.get_transaction_by_id)
]
