from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Transaction(models.Model):

    # ========================================
    # ENUMS
    # ========================================

    # Criação enum do tipo de transição
    class TransactionType(models.TextChoices):
        INCOME = 'income', 'Entrada'
        EXPENSE = 'expense' 'Saída'

    # ========================================
    # CAMPOS
    # ========================================
    
    id = models.BigAutoField(primary_key=True)

    description = models.CharField(
        max_length=255, 
        verbose_name="Descrição"
    )
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Valor",
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    type = models.CharField(
        max_length=7,           
        choices=TransactionType.choices,
        verbose_name="Tipo"
    )
    
    date = models.DateField(
        verbose_name="Data"
    )

    def __str__(self):
        return f"{self.description} ({self.get_type_display()} - {self.amount})"