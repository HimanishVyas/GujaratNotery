# Generated by Django 5.0.6 on 2024-07-07 04:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=50, verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=50, verbose_name='District')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='User Name')),
                ('business_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Business Firm Name')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last Name')),
                ('email', models.CharField(max_length=100, unique=True, verbose_name='Email')),
                ('password', models.CharField(max_length=500, verbose_name='Password')),
                ('other_email', models.CharField(blank=True, max_length=100, null=True, verbose_name='Other Email')),
                ('user_role', models.CharField(choices=[('notery', 'Notery'), ('stemp_vender', 'Stemp Vender'), ('stationary_vender', 'Stationary Vender')], max_length=100, verbose_name='User Role')),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Profile IMG')),
                ('user_phone', models.CharField(blank=True, max_length=13, null=True, verbose_name='User Phone number')),
                ('notery_reg_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Notary Reg. Number')),
                ('estamp_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Estamp Reg. Number')),
                ('office_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Office Address')),
                ('user_reg_status', models.CharField(blank=True, choices=[('all_done', 'All Done'), ('payment_done', 'Payment Done'), ('payment_pending', 'Payment Pending')], max_length=100, null=True, verbose_name='User Registrations Status')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser Status')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.country', verbose_name='Country')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.district', verbose_name='District')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_start_date', models.DateTimeField(blank=True, null=True, verbose_name='Order Start Date')),
                ('order_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Order Start Date')),
                ('durations', models.IntegerField(default=1, verbose_name='Durations In Year')),
                ('user_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=50, verbose_name='State')),
                ('country_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.country', verbose_name='Country')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='state_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.state', verbose_name='State'),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.state', verbose_name='State'),
        ),
    ]
