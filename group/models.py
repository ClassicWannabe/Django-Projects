from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.shortcuts import reverse
from time import time
# Create your models here.
User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField()
    user = models.ManyToManyField(User,through='GroupMember')
    author = models.CharField(max_length=20,null=True)

    def get_absolute_url(self):
        return reverse('groups:group_detail_url',kwargs={'slug':self.slug,'pk':self.pk})

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name,allow_unicode=True)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name+' by '+self.author

    class Meta:
        ordering = ['name']

class GroupMember(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " " + self.group.name
    class Meta:
        unique_together = ('user','group')
