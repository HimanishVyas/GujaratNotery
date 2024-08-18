from django.db import models
from django.db.models.signals import post_save
import datetime
from django.dispatch import receiver
from user import choice
from django.contrib.auth.models import AbstractBaseUser
from user.managers import UserManager


# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=50, verbose_name="Country")

    def __str__(self):
        return str(self.country_name)


class State(models.Model):
    country_fk = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Country")
    state = models.CharField(max_length=50, verbose_name="State")

    def __str__(self):
        return str(self.state)


class District(models.Model):
    state_fk = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="State")
    district = models.CharField(max_length=50, verbose_name="District")

    def __str__(self):
        return str(self.district)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, verbose_name="User Name", null=True, blank=True)
    business_name = models.CharField(max_length=200, verbose_name="Business Firm Name", null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name="First Name", null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Last Name", null=True, blank=True)
    email = models.CharField(max_length=100, verbose_name="Email", unique=True)
    password = models.CharField(max_length=500, verbose_name="Password")
    other_email = models.CharField(max_length=100, verbose_name="Other Email", null=True, blank=True)
    user_role = models.CharField(max_length=100, verbose_name="User Role", choices=choice.UserRole)
    profile_img = models.ImageField(verbose_name="Profile IMG", null=True, blank=True)
    user_phone = models.CharField(max_length=13, verbose_name="User Phone number", null=True, blank=True)
    notery_reg_number = models.CharField(max_length=50, verbose_name="Notary Reg. Number", null=True, blank=True)
    estamp_number = models.CharField(max_length=50, verbose_name="Estamp Reg. Number", null=True, blank=True)
    office_address = models.CharField(max_length=500, verbose_name="Office Address", null=True, blank=True)
    user_reg_status = models.CharField(max_length=100, verbose_name="User Registrations Status",
                                       choices=choice.UserREGStatus, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name="Country", null=True, blank=True)
    state = models.ForeignKey(State, verbose_name="State", null=True, blank=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(District, verbose_name="District", null=True, blank=True, on_delete=models.SET_NULL)
    is_staff = models.BooleanField(verbose_name="Staff Status", default=False)
    is_superuser = models.BooleanField(verbose_name="Superuser Status", default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        "password",
        "user_phone",
        "user_role",
        "business_name",
        "first_name",
        "last_name",
    ]

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def __str__(self):
        return str(self.username) if self.username else str(self.id)


@receiver(post_save, sender=User)
def create_username(sender, instance, created, **kwargs):
    if created:
        try:
            year = datetime.date.year
            instance.username = (
                f"{instance.first_name}_{instance.id}")
            instance.save()
        except Exception as e:
            print(e)


post_save.connect(create_username, sender=User)


class MemberShip(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    order_start_date = models.DateTimeField(verbose_name="Order Start Date", null=True, blank=True)
    order_end_date = models.DateTimeField(verbose_name="Order Start Date", null=True, blank=True)
    durations = models.IntegerField(verbose_name="Durations In Year", default=1)

    def __str__(self):
        return f"{self.user_fk}-{order_start_date}-{order_end_date}"


class Logs(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    activity = models.CharField(verbose_name="Activity", max_length=500, null=True, blank=True)
    date_time = models.DateTimeField(verbose_name="Date Time Stemp", auto_now_add=True, null=True, blank=True)
