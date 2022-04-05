from garpix_order.models.payment import Payment
from django.dispatch import receiver
from django.db import models
from . import Order, Payment
from user.models.profile import Profile



@receiver(models.signals.pre_delete, sender=Order)
def delete_question(sender, instance, using, **kwargs):
    try:
        payment = Payment(order=instance)
        payment.delete()
        instance.delete()
    except:
        pass


@receiver(models.signals.post_save, sender=Payment)
def update_balance(sender, instance, created, **kwargs):
    #payment = instance
    if instance.status == 1:
        cash = instance.cost
        instance.profile.balance = instance.profile.balance + cash
        instance.profile.save()
