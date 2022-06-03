from datetime import datetime
from rest_framework import serializers
from . models import Note


class NoteSerializer(serializers.ModelSerializer):
    nt_author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("nt_author", )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        nt_createtime = datetime.strptime(ret['nt_createtime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        nt_updatetime = datetime.strptime(ret['nt_updatetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['nt_createtime'] = nt_createtime.strftime('%d %B %Y %H:%M:%S')
        ret['nt_updatetime'] = nt_updatetime.strftime('%d %B %Y %H:%M:%S')
        return ret


class NoteDetailSerializer(serializers.ModelSerializer):
    nt_author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("nt_author",)

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        nt_createtime = datetime.strptime(ret['nt_createtime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        nt_updatetime = datetime.strptime(ret['nt_updatetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['nt_createtime'] = nt_createtime.strftime('%d %B %Y %H:%M:%S')
        ret['nt_updatetime'] = nt_updatetime.strftime('%d %B %Y %H:%M:%S')
        return ret