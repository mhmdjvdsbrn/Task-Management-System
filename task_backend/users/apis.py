from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import RegexValidator, MinLengthValidator
from task_backend.users.models import BaseUser, Profile
from task_backend.api.mixins import ApiAuthMixin
from task_backend.users.selectors import get_profile
from task_backend.users.services import register, update_profile
from task_backend.users.general_serializer import UserSerializer, ChangePhoneSerializer
from task_backend.users.validators import validate_phone_number, special_char_validator, letter_validator,number_validator
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from drf_spectacular.utils import extend_schema

# # Custom phone number validator
# phone_validator = RegexValidator(
#     regex=r'^09\d{9}$',
#     message="Phone number must be 11 digits and start with '09'."
# )

# ------Register-API---------

class RegisterApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        phone = serializers.CharField(
            max_length=11,
            validators=[validate_phone_number]
        )
        password = serializers.CharField(
            validators=[
                number_validator,
                letter_validator,
                special_char_validator,
                MinLengthValidator(limit_value=8)
            ]
        )
        confirm_password = serializers.CharField(max_length=255)

        def validate_phone(self, phone):
            if BaseUser.objects.filter(phone=phone).exists():
                raise serializers.ValidationError("Phone number already taken")
            return phone

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("Confirm password does not match password")
            return data

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser
            fields = ("phone", "token", "register_date")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                phone=serializer.validated_data.get("phone"),
                password=serializer.validated_data.get("password"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutPutRegisterSerializer(user, context={"request": request}).data)


# ------Profile-API---------

class CompleteProfileApi(ApiAuthMixin, APIView):
    class InputCompleteProfileSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=50)
        last_name = serializers.CharField(max_length=50)
        gender = serializers.ChoiceField(choices=Profile.GENDER_CHOICES)
        avatar = serializers.ImageField(use_url=True, required=False)

    class OutputCompleteProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('first_name', 'last_name', 'gender', 'avatar')

    @extend_schema(request=InputCompleteProfileSerializer, responses=OutputCompleteProfileSerializer)
    def put(self, request):
        serializer = self.InputCompleteProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            profile = update_profile(
                user=request.user.pk,
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                gender=serializer.validated_data.get("gender"),
                avatar=serializer.validated_data.get("avatar"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputCompleteProfileSerializer(profile, context={"request": request}).data)

class ViewProfileApi(ApiAuthMixin, APIView):
    class OutputViewProfileSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)

        class Meta:
            model = Profile
            fields = ('user', 'first_name', 'last_name', 'gender', 'avatar')

    @extend_schema(
        responses=OutputViewProfileSerializer,
    )
    def get(self, request):
        try:
            query = get_profile(user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Not Found -- " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.OutputViewProfileSerializer(query)

        return Response(serializer.data)
