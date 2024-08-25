

from rest_framework import serializers
from task_backend.users.models import BaseUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'phone',)


class ChangePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields= ['phone']