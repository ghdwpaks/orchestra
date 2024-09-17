from .models import *
from rest_framework import serializers
from django.db.models import Q

from rest_framework import serializers

class UserDefSer(serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = ("id","nickname")

class UserDetailSer(serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = ("id","nickname","email","credate","deldate","is_active","is_deleted")

#

class VidDefSer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:user-list', source='username',
                                                lookup_url_kwarg='username', lookup_field='username')

    class Meta:
        model = Vid
        fields = ('id', 'name', 'url')

class VidDetailSer(serializers.ModelSerializer):
    class Meta:
        model = Vid
        fields = ('id', 'name', 'url')

#

class HighDefSer(serializers.ModelSerializer):
    class Meta:
        model = High
        fields = ('id', 'timestamp')

class HighDetailSer(serializers.ModelSerializer):
    class Meta:
        model = High
        fields = ('id', 'timestamp')

#
class TagFunc():
    def get_name(obj, context):
        l = context[0].get("l", 1)
        tagNames = TagName.objects.filter(
            Q(tag_id=obj.id) & Q(lang=l)
        )
        return tagNames.first().name if tagNames.exists() else ""
    
    def get_url(obj):return obj.url

class TagDefSer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    def get_name(self, obj):
        return TagFunc.get_name(obj, self.context)  # context 전달

    class Meta:
        model = Tag
        fields = ('name',)


class TagDetailSer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    def get_name(self, obj):
        return TagFunc.get_name(obj, self.context)  # context 전달

    class Meta:
        model = Tag
        fields = ('id', 'name')

#

class TagNameDefSer(serializers.ModelSerializer):
    class Meta:
        model = TagName
        fields = ("name")

class TagNameDetailSer(serializers.ModelSerializer):
    class Meta:
        model = TagName
        fields = ("lang","name")

#

class MemoDefSer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ("content")

class MemoDetailSer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ("user","vid","content")

#

class CommentDefSer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content")

class CommentDetailSer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("user","vid","public_visible","content")

class LogDefSer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ("user","action_type","action_obj","field_type","before","after")
'''
class LogDetailSer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ("user","action_type","action_obj","field_type","before","after")
'''
