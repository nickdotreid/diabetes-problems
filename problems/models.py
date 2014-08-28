from django.db import models

from sorl.thumbnail import ImageField

from django.db.models.signals import pre_save, post_save, pre_delete
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'
        ordering = ['title']

    title = models.CharField(blank=True, max_length=150)
    image = ImageField(
        blank=True,
        null=True,
        upload_to="problems",
        )

    def __unicode__(self):
        return self.title

class Session(models.Model):
    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'

    key = models.CharField( unique=True, max_length=30)
    user = models.ForeignKey(User, blank=True, null=True)

    def problems(self):
        try:
            return Problem.objects.filter(important__session=self).all()
        except:
            return []

    def email_add(self, email):
        try:
            user, created = User.objects.get_or_create(username=email, email=email)
            self.user = user
            self.save()
        except:
            return False
        return True


    def __unicode__(self):
        if self.user and self.user.email:
            return "%s: %s" % (self.user.email, self.key)
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

class Important(models.Model):
    class Meta:
        verbose_name = 'Important'
        verbose_name_plural = 'Importants'

    problem = models.ForeignKey(Problem)
    session = models.ForeignKey(Session)

    ranking = models.IntegerField(blank=True, null=True, default=0)

    def __unicode__(self):
        return unicode(self.session) + unicode(self.problem)

class PersonType(models.Model):
    name = models.CharField(unique=True, max_length=50, default="")

    def __unicode__(self):
        return self.name
    

class Survey(models.Model):
    session = models.ForeignKey(Session, null=True, blank=True)
    person_types = models.ManyToManyField(PersonType)
    birth_year = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return ",".join([ x.name for x in self.person_type.all()])

class Suggestion(models.Model):
    class Meta:
        verbose_name = 'Suggestion'
        verbose_name_plural = 'Suggestions'

    session = models.ForeignKey(Session)
    submitted = models.DateTimeField(auto_now=True, auto_now_add=True)
    description = models.CharField(max_length=500)

    problems = models.ManyToManyField(Problem)


    def __unicode__(self):
        return self.description
    
    
    

    