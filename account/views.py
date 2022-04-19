from account.serializers import UserRegisterSerializer , UserLoginSerializer ,CurrentUserSerializer ,ChangePasswordSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


# Create your views here.

# User Registration View 
class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"message": "User Registered!"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors ,status.HTTP_400_BAD_REQUEST)


# User Login View

class UserLoginView(APIView):
    def post(self , request ):
        serializer = UserLoginSerializer(data= request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                tokens = get_tokens_for_user(user)
                return Response({'message':'Login Successful',"tokens":tokens},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Passoword is incorrect']}},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

#  Get Current User View

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data , status= status.HTTP_200_OK)


# Change Current User Password

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):
        serializer = ChangePasswordSerializer(data= request.data,context= {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
