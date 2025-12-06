from django.urls import path

from . import views

urlpatterns = [
    path('', views.transactions_manager),
    path('<int:id>/', views.transaction_specific_manager)
]
