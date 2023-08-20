import string
import time
from django.contrib.auth import login, logout
from django.utils import timezone
import random

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import CustomUser, InvitationCode
from api.serializers import UserProfileSerializer, SendVerificationCodeSerializer, \
    AuthenticateWithVerificationCodeSerializer, invatedCodeSerializer


class SendVerificationCodeView(APIView):
    serializer_class = SendVerificationCodeSerializer

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if phone_number:
            time.sleep(2)
            verification_code = ''.join(random.choices(string.digits, k=4))

            try:
                user = CustomUser.objects.get(phoneNumber=phone_number)
                user.verification_code = verification_code
                user.verification_code_sent_at = timezone.now()
                user.save()
                return Response(
                    {"message": "Verification code sent to your phone number.", "verification_code": verification_code}
                )
            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create(phoneNumber=phone_number,
                                                 verification_code=verification_code,
                                                 verification_code_sent_at=timezone.now())
                invitation_code = InvitationCode.generate_code()
                invitation_code_instance = InvitationCode.objects.create(code=invitation_code)
                user.invitation_code_self = invitation_code_instance
                user.save()
                return Response(
                    {"message": "Hello new user, verification code sent to your phone number.",
                     "verification_code": verification_code}
                )
        return Response({"message": "Please provide a phone number."}, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateWithVerificationCodeView(APIView):
    serializer_class = AuthenticateWithVerificationCodeSerializer

    def post(self, request):
        verification_code = request.data.get('verification_code')
        if verification_code:
            try:
                custom_user = CustomUser.objects.get(
                    verification_code=verification_code,
                    verification_code_sent_at__gte=timezone.now() - timezone.timedelta(minutes=5)
                )
                login(request, custom_user)
                return Response({"message": "You have been successfully authenticated."})
            except CustomUser.DoesNotExist:
                return Response({"message": "Invalid verification code or code expired."},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Please provide a verification code."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "You have been successfully logout"}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    serializer_class = invatedCodeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        invitation_code = request.data.get('invitation_code_other')

        if user.invitation_code_other is not None:
            return Response({"message": "Invated code can only add 1 time"}, status=status.HTTP_400_BAD_REQUEST)

        if user.invitation_code_self.code == invitation_code:
            return Response({"message": "Can't use self-invited code"}, status=status.HTTP_400_BAD_REQUEST)

        if invitation_code:
            try:
                invitation_code_instance = InvitationCode.objects.get(code=invitation_code)
                user.invitation_code_other = invitation_code_instance
                user.save()

                return Response({"message": "Invated code is successfully added."})
            except InvitationCode.DoesNotExist:
                return Response({"message": "Invalid invitation code."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Please provide an invitation code."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileRefsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        authenticated_user = request.user
        authenticated_user_invitation_code = authenticated_user.invitation_code_self
        matching_users = CustomUser.objects.filter(invitation_code_other__code=authenticated_user_invitation_code.code)
        phone_numbers = [user.phoneNumber for user in matching_users]
        return Response(phone_numbers)
