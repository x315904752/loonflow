from rest_framework import serializers

from apps.account.models import LoonUser


class LoonUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoonUser
        fields = '__all__'
