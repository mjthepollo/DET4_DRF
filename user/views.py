from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
from user.models import User
from user.serializer import UserSerializer


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


class UserLoginAPI(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        # 만약 username에 맞는 user가 존재하지 않는다면,
        if user is None:
            return Response(
                {"message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호가 틀린 경우,
        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # user가 맞다면,
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)  # refresh 토큰 생성
            refresh_token = str(token)  # refresh 토큰 문자열화
            access_token = str(token.access_token)  # access 토큰 문자열화
            response = Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "login success",
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response(
                {"message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
