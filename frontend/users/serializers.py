from rest_framework import serializers
from .models import User, Role, Action
from servers.models import Server
from servers.serializers import ServerSerializer


class UserSerializer(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Action.objects.all(),
        required=True
    )
    servers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Server.objects.all(),
        required=True
    )

    # debugging
    server_details = ServerSerializer(
        source='servers', 
        many=True, 
        read_only=True
    )

    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }
    
    def create(self, validated_data):
        actions = validated_data.pop('actions')
        servers = validated_data.pop('servers')

        user = User.objects.create(
            username=validated_data['username'],
            password='defaultpassword',  # Set a default password
            **validated_data
        )

        user.actions.set(actions)
        user.servers.set(servers)
        
        return user
