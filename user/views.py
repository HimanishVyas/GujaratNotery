from django.shortcuts import render

# Create your views here.
import datetime
from django_filters.rest_framework import DjangoFilterBackend
# Import Models
from user.models import (
    User,
    Country,
    State,
    District,
    MemberShip,
    Logs
)
# Import password validation and auth methods
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate

# DRF imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

# Serializer Import
from user.serializer import (
    UserSerializer
)

from user.auth import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token
)


# Ganrate Token

def get_tokens_for_user(user):
    # refresh = RefreshToken.for_user(user)
    # access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    id = decode_refresh_token(refresh_token)
    refresh_access_token = create_access_token(id)

    return {
        "refresh": refresh_token,
        "access": refresh_access_token,
    }


class LoginApi(ViewSet):
    authentication_classes = []

    def create(self, request):
        password = request.data.get("password")
        if request.data.get("email"):
            email = request.data.get("email")
            user = User.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    user_serializer = UserSerializer(
                        user, context={"request": request}
                    )
                    token = get_tokens_for_user(user)
                    response = user_serializer.data
                    response["token"] = token
                    # creating logs
                    Logs.objects.create(user_fk=user, activity="Logged In")
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "Password not Match"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "NO user With this Email ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"message": "Your Email ID is not registered"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserListing(ModelViewSet):
    authentication_classes = []
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'business_name', 'first_name', 'last_name', 'user_role', 'country__country_name',
                        'state__state',
                        'district__district']

    def get_queryset(self):
        return User.objects.all()  # Return the queryset here

    # def list(self, request, *args, **kwargs):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.get(id=pk)
    #     serializer = UserSerializer(queryset)
    #     return Response(serializer.data)
