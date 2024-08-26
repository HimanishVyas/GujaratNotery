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
from django.shortcuts import get_object_or_404

# Serializer Import
from user.serializer import (
    UserSerializer,
    UserCreateSerializer
)

from user.auth import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token
)


# Ganrate Token

def get_tokens_for_user(user):
    refresh_token = create_refresh_token(user.id)
    id = decode_refresh_token(refresh_token)
    refresh_access_token = create_access_token(id)

    return {
        "refresh": refresh_token,
        "access": refresh_access_token,
    }


class CreateUserApi(ViewSet):
    def create(self, request):
        data = request.data
        # checking if email and username exsiting or not 
        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Email already exists", "status": status.HTTP_400_BAD_REQUEST})
        elif User.objects.filter(username=data["username"]).exists():
            return Response({"error": "Username already exists", "status": status.HTTP_400_BAD_REQUEST})
        
        # country = Country.objects.filter(country_name=data["country"])
        # if country == None:
        #     country = Country.objects.create(country_name=data["country"]) # creating non exsiting country

        # state = State.objects.filter(state=data["state"], country_fk=country)
        # print(state, "============")
        # if state == None:
        #     print(data["state"])
        #     state = State.objects.create(state=data["state"], country_fk=country[0]) # creating non exsiting state
            
        # district = District.objects.get(state_fk=state[0], district=data["district"])        
        # if district == None:
        #     district = District.objects.create(state_fk=state, district=data["district"]) # creating non exsiting state
        
        country = Country.objects.get(country_name=data["country"])
        state = State.objects.get(country_fk=country, state=data["state"])
        district = District.objects.get(district=data["district"], state_fk=state)
        data['country'] = country.id
        data['state'] = state.id
        data['district'] = district.id
        data['user_reg_status'] = 'user_reg_status'
        user_serializer = UserCreateSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        token = get_tokens_for_user(user)
        response = user_serializer.data
        response["token"] = token
        response["status"] = status.HTTP_201_CREATED
        response["message"] = "User Created successfully"
        return Response(response, status=status.HTTP_200_OK)
    
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
    filterset_fields = ['username',
                        'business_name',
                        'first_name',
                        'last_name',
                        'user_role',
                        'country__country_name',
                        'state__state',
                        'district__district'
                        ]

    def get_queryset(self):
        return User.objects.all()  # Return the queryset here

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response = {
            "data": serializer.data,
            "count": queryset.count(),
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    #
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user)
        response = {
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

