from rest_framework import serializers

from apps.account.models import LoonUser, AppToken


class LoonUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoonUser
        fields = '__all__'
