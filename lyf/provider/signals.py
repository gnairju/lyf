# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from user.models import CustomUser  # Import your CustomUser model
from adminPanel.models import Product
from django.urls import reverse
from order.models import order

@receiver(post_save, sender=Product)
def send_new_product_email(sender, instance, created, **kwargs):
    if created:
        # Send email to admin
        user = instance.user
        subject = 'New Product Added'
        message = f'New product "{instance.title}" added by {user.first_name}.'
        message += f' Please <a href="http://127.0.0.1:8000/performlogin">login</a> to activate.'

        from_email = 'o23211671@gmail.com'  
        email = 'lyfrentals04@gmail.com'

        send_mail(subject, message, from_email, [email])


@receiver(post_save, sender=order)
def send_new_rental_email(sender, instance, created, **kwargs):
    if created:
        # Send email to admin
        user = instance.user
        subject = 'New Rental'
        message = f'New rental "{instance.product}" by {user.first_name}.'
        message += f' Please login to activate: <a href="http://127.0.0.1:8000/performlogin">Login</a>'

        from_email = 'o23211671@gmail.com'  
        email = instance.product.user
        send_mail(subject, message, from_email, [email])

