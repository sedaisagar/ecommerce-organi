from rest_framework import serializers

from users.models import User
from django.contrib.auth.hashers import make_password

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ["first_name", "last_name", "email", "username", "password", "role"]
        extra_kwargs = {
            "password":{
                "write_only":True,
            },
            "role": {
                "read_only":True,
            }
        }


    def create(self, validated_data:dict):
        password = validated_data.pop("password", "")

        validated_data["password"] = make_password(password)
        
        # Below line saves the object in db
        return super().create(validated_data)