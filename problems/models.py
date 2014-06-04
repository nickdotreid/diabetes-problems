from django.db import models

from django.db.models.signals import pre_save, post_save, pre_delete
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'

    title = models.CharField(blank=True, max_length=150)
    image = models.ImageField(blank=True, upload_to="problems")

    def __unicode__(self):
        return self.title

class Session(models.Model):
    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'

    key = models.CharField( unique=True, max_length=30)
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.key
        
def session_make_key():
	key = User.objects.make_random_password(30)  #make a random string the size of key field
	try:
		Session.objects.get(key=key) # if this key is in use, recurse
		return session_make_key()
	except:
		return key

def session_create_key(sender, instance, **kwargs):
	if 'raw' in kwargs and kwargs['raw']:
		return
	if not instance.key:
		instance.key = User.objects.make_random_password(30)
pre_save.connect(session_create_key, sender=Session)
    