from rest_framework import serializers
from .models import CustomUser, Children, Parents


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'is_parent', 'is_child']

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = "__all__"


class ChildSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(source='parent_id', read_only=True)
    class Meta:
        model = Children
        fields = '__all__'




