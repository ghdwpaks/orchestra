
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from .musicbooks.obsessive import is_hashed
import os
import binascii

from django.utils import timezone
from datetime import timedelta

# Create your models here.
class User(AbstractBaseUser) :
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    uid = models.CharField(max_length=50,default=None)
    password = models.CharField(max_length=128)
    nickname = models.CharField(max_length=50,default="사용자",blank=True)
    email = models.CharField(max_length=50,default="def@def",blank=True, unique=True)
    credate = models.DateTimeField(auto_now_add=True, verbose_name="등록시각")
    deldate = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.nickname}({self.id})"
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "user"

    api_modifiable_fields = ["nickname","email"]
    @classmethod
    def get_api_modifiable_fields(cls):
        return cls.api_modifiable_fields

class UserToken(models.Model):
    key = models.CharField(max_length=128, null=True, blank=True, unique=True)
    user = models.ForeignKey(User, related_name='userTokens',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="등록시각")
    useable = models.BooleanField(default=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.key : 
            self.key = binascii.hexlify(os.urandom(64)).decode()
        return super().save(*args, **kwargs)
    
    def __str__(self) : return self.key

    @property
    def is_authenticated(self): return True


class Vid(models.Model) :
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=20,blank=True)
    url = models.CharField(max_length=100,blank=True)
    
    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        verbose_name = "vid"
        verbose_name_plural = "vid"

class High(models.Model) :
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    vid = models.ForeignKey(Vid, on_delete=models.CASCADE, related_name='highlights')
    timestamp = models.IntegerField(default=None, verbose_name="timestamp")
    
    def __str__(self):
        return f"{self.vid_id}:{self.id}"
    
    class Meta:
        verbose_name = "high"
        verbose_name_plural = "high"

class Tag(models.Model) :
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    vid = models.ForeignKey(Vid, null=True, default=None, blank=True, on_delete=models.CASCADE, related_name='tags')
    high = models.ForeignKey(High, null=True, default=None, blank=True, on_delete=models.CASCADE, related_name='tags')
    
    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tag"
    
class TagName(models.Model) :
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tagNames')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagNames')
    lang = models.IntegerField(default=0, blank=True, verbose_name="태그언어")#1:한국어,2:영어,3:일본어
    name = models.CharField(max_length=30,blank=True)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "tagName"
        verbose_name_plural = "tagName"
    
class Memo(models.Model) :
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memos')
    vid = models.ForeignKey(Vid, on_delete=models.CASCADE, related_name='memos')
    content = models.CharField(max_length=200,blank=True)
    
    def __str__(self):
        return f"{self.content}"
    
    class Meta:
        verbose_name = "memo"
        verbose_name_plural = "memo"

class Comment(models.Model) :
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    vid = models.ForeignKey(Vid, on_delete=models.CASCADE, related_name='comments')
    public_visible = models.BooleanField(default=False)
    content = models.CharField(max_length=200,blank=True)
    
    models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.SET_NULL, verbose_name="온보딩 담당자", limit_choices_to={'groups__name': "온보딩팀"})
    


    def __str__(self):
        return f"{self.content}"
    
    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comment"

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    confirmable = models.BooleanField(default=True) #검사할때 사용할 수 있는지
    useable = models.BooleanField(default=True) #패스워드를 변경할때 사용할 수 있는지
    created_at = models.DateTimeField(auto_now_add=True)
    '''
    @classmethod
    def delete_expired_codes(cls):
        cls.objects.filter(created_at__lt=timezone.now()-timedelta(minutes=3)).delete()
    '''

class Log(models.Model) :
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    action_type = models.IntegerField(default=0, blank=True, verbose_name="행동양식")#1:생성,2:수정,3:삭제
    action_obj = models.IntegerField(default=0, blank=True, verbose_name="행동주체")
    field_type = models.IntegerField(default=0, blank=True, verbose_name="행동주체의 필드번호. 위에서 0부터 오름차순.")
    before = models.CharField(max_length=200,blank=True)
    after = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return f"{self.action_type}"
    
    class Meta:
        verbose_name = "log"
        verbose_name_plural = "log"
    

'''
action_obj ->
User:0
Vid:1
Highlight:2
Tag:3
TagName:4
Memo:5
Comment:6
'''