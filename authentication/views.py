from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer

from random_username.generate import generate_username

@api_view(['GET'])
def protected(request):
    if request.user.is_anonymous:
        return Response({'message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    return Response({'message': 'This is a protected endpoint.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # create profile with blank values
    Profile.objects.create(user=serializer.instance, username=generate_username(1)[0])
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
def my_profile(request):
    if request.user.is_anonymous:
        return Response({'message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        print(request.query_params)
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        parser_classes = (MultiPartParser, FormParser)
        print(request.data)
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)