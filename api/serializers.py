from django.db.models import Prefetch
from rest_framework import serializers

from api.models import CustomUser


class SendVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=1000,
        style={'base_template': 'textarea.html'}
    )


class AuthenticateWithVerificationCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=1000,
                                              style={'base_template': 'textarea.html'})


class invatedCodeSerializer(serializers.Serializer):
    invitation_code = serializers.CharField(max_length=1000,
                                            style={'base_template': 'textarea.html'})


class UserProfileSerializer(serializers.ModelSerializer):
    invitation_code_self = serializers.SerializerMethodField()
    invitation_code_other = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_invitation_code_other(self, obj):
        invitation_code_instance = obj.invitation_code_other

        if invitation_code_instance:
            return invitation_code_instance.code
        return None

    def get_invitation_code_self(self, obj):
        invitation_code_instance = obj.invitation_code_self

        if invitation_code_instance:
            return invitation_code_instance.code
        return None
