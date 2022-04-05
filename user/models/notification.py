from django.db import models
from .profile import Profile
from django.dispatch import receiver


class Notification(models.Model):

    profile = models.ForeignKey(
        Profile, verbose_name='Профиль пользователя', related_name='notifications', on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(verbose_name='Текст уведомления', max_length=255, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)
    is_all = models.BooleanField(verbose_name='Всем', default=False)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-id',]

    def __str__(self):
        return f'{self.created_at} {self.profile} - {self.message}'

@receiver(models.signals.post_save, sender=Notification)
def send_all(sender, instance, using, **kwargs):
    if instance.is_all == True:
        profiles = Profile.objects.all()
        for profile in profiles:
            if instance.profile != profile:
                notification = Notification(profile=profile, message=instance.message, created_at=instance.created_at)
                notification.save()
