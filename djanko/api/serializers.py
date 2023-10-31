from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        extra_kwargs = {'hanko_id': {'read_only': True}}

    def create(self, validated_data):                              
        user = User.objects.create(
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name')
        )                     
        user.hankoprofile.hanko_id = validated_data.get('hanko_id')
        user.save()
        return user