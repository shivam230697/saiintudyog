from django.db import models
from django.utils import timezone


# Create your models here.

class AccountModel(models.Model):
    type_choice = [
        ('SALE', 'Sale'),
        ('MITTI', 'Mitti'),
        ('TURI', 'Turi')
    ]
    account_id = models.CharField(max_length=15, unique=True, editable=False)  # ID format: YYYYMMDD-XXX
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=type_choice, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def generate_account_id():
        # Get the current date in the format YYYYMMDD
        date_str = timezone.now().strftime("%Y%m%d")

        # Get the highest existing ID number for today
        existing_ids = AccountModel.objects.filter(account_id__startswith=date_str).order_by('-account_id')

        if existing_ids.exists():
            # Extract the last 3 digits of the highest existing ID and increment
            last_id = existing_ids.first().account_id
            last_number = int(last_id[len(date_str):])  # Extract the number after the date part
            new_number = str(last_number + 1).zfill(3)  # Increment and zero-fill to 3 digits
        else:
            # If no IDs exist for today, start with 001
            new_number = '001'

        # Combine the date and new number to create the new account ID without a hyphen
        return f"{date_str}{new_number}"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.account_id:
            self.account_id = self.generate_account_id()
        super().save(*args, **kwargs)
