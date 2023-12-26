from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name


    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                email_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved:
                    email_subject = 'Congratulations! Your restaurant has been approved.'
                    # send notification
                    send_notification(email_subject, email_template, context)
                else:
                    email_subject = 'We are sorry! You are not eligible for publishing your food menu on our marketplace.'
                    # send notification
                    send_notification(email_subject, email_template, context)
        # This supper method will actually allow you to access the save method of this particular class.
        return super(Vendor, self).save(*args, **kwargs)


