from django.db import models
from django.contrib.auth import get_user_model
from group.models import Group
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
User = get_user_model()

class Post(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group,related_name='posts',null=True,on_delete=models.CASCADE)
    # picture = models.ImageField(upload_to='posts',null=True,blank=True)

    def get_absolute_url(self):
        return reverse('groups:group_detail_url',kwargs={'slug':self.group.slug,'pk':self.group.pk})

    def get_image_filename(instance,filename):
        name = instance.post.name
        slug = slugify(name)
        return f'posts/{slug}-{filename}'

    def __str__(self):
        return self.name+' by '+self.user.username

    class Meta:
        ordering = ['-date']

class Image(models.Model):
    post = models.ForeignKey(Post,related_name='image',on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=Post.get_image_filename)

    def __str__(self):
        return self.post.name
