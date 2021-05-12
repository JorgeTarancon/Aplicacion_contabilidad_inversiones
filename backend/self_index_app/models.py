from django.db import models

# Create your models here.
class Investor(models.Model):
    investor_id = models.AutoField(primary_key=True)
    worth = models.FloatField(max_length=14)

class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    amount = models.FloatField()
    asset_name = models.CharField(max_length = 200)