from django.db import models

class UserRole(models.TextChoices):
    NOTERY = "notery", "Notery"
    STEMP_VENDER = "stemp_vender", "Stemp Vender"
    stationary_vender = "stationary_vender", "Stationary Vender"
    
class UserREGStatus(models.TextChoices):
    ALL_DONE = "all_done", "All Done"
    PAYMENT_DONE = "payment_done", "Payment Done"
    PAYMENT_PENDING = "payment_pending", "Payment Pending"