from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializer import UserSerializer, UserSerializerWithToken, ImageSerializer
from rest_framework import status
from .models import UserProfileImage
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter,OrderingFilter


# @api_view(['GET'])
def getRoutes(request):
    return JsonResponse('heoo', safe=False)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_admin'] = user.is_superuser

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer=UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v       
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
   

@api_view(['POST'])
def register(request):
    data = request.data
    print(data)
    try:
        user = User.objects.create(first_name=data['fname'], last_name=data['lname'], username=data['email'], email=data['email'], password=make_password(data['password']))
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'details': "User Already Exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUserProfile(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    try:
        user_profile = UserProfileImage.objects.get(user=user)
        image_serializer = ImageSerializer(user_profile)
        response = {
            'user': serializer.data,
            'user_img': image_serializer.data
        }
    except UserProfileImage.DoesNotExist:
        response = {
            'user': serializer.data,
            'user_img': None
        }
    return Response(response)


class UserProfileView(RetrieveUpdateAPIView):
    queryset = UserProfileImage.objects.all()
    serializer_class = ImageSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user_profile = UserProfileImage.objects.filter(user_id=pk).order_by('-created_at').first()
            user_serializer = UserSerializer(user)
            image_serializer = ImageSerializer(user_profile)
            response = {
                'user': user_serializer.data,
                'user_img': image_serializer.data
            }
        except UserProfileImage.DoesNotExist:
            user = User.objects.get(id=pk)
            user_serializer = UserSerializer(user)
            response = {
                'user': user_serializer.data,
                'user_img': None
            }

        return Response(response)

    def post(self, request, pk):
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', image_serializer.errors)
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


@api_view(['GET'])
@permission_classes((IsAuthenticated, IsAdminUser))
def getUsers(request):
    user = User.objects.filter(is_superuser=False)
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


# class ClassUserList(ListCreateAPIView):
#     queryset=User.objects.filter(is_superuser=False)
#     serializer_class=UserSerializer
#     filter_backends=[SearchFilter]
#     search_fields=['username','email']




@api_view(['PUT'])
def userUpdate(request,pk):
    try:
        data=request.data
        user=User.objects.get(id=pk)
        serializer=UserSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response("User not found!",status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def userDelete(request,pk):
    try:
        user = User.objects.exclude(id=1).get(id=pk)
        user.delete()
        return Response('User deleted')
    except User.DoesNotExist:
        return Response("User not found")


class ClassUserList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset=User.objects.filter(is_superuser=False)
    serializer_class=UserSerializer
    filter_backends=[SearchFilter]
    search_fields=['username','email']