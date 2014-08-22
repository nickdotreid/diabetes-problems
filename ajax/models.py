from main.views import pre_template_render
from django.dispatch import receiver

@receiver(pre_template_render)
def change_template(sender, **kwargs):
    print("Request finished!")
    if 'template' in kwargs and kwargs['template'] == 'base.html':
    	return "ajax.html"
    return False
