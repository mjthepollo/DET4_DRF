from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
from user.models import User
from user.serializer import (UserInfoSerializer, UserLoginSerializer,
                             UserSignUpSerializer)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserSignupAPI(APIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            email = request.data['email']

            user = User.objects.filter(username=username).first()

            if user:
                return Response({
                    "status": "error",
                    "message": "User ID Already Exists"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                return Response({
                    "status": "success",
                    "message": "User registered successfully",
                    "data": UserInfoSerializer(user).data
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPI(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        # 만약 username에 맞는 user가 존재하지 않는다면,
        if user is None:
            return Response(
                {"status": "error", "message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호가 틀린 경우,
        if not check_password(password, user.password):
            return Response(
                {"status": "error", "message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # user가 맞다면,
        if user is not None:
            response = Response(
                {
                    "status": "success",
                    "message": "User logged in succesfully",
                    "data": UserInfoSerializer(user).data,
                },
                status=status.HTTP_200_OK
            )
            return response
        else:
            return Response(
                {"status": "error", "message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
