from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
# import pagination stuff
from rest_framework.pagination import PageNumberPagination
# import search stuff
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Post
from authentication.models import Profile
from .serializers import PostSerializer, CreatePostSerializer

@api_view(['GET', 'POST'])
def posts(request, username=None):
    if request.user.is_anonymous:
        return Response({'message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':

        if username != None:
            try:
                profile = Profile.objects.get(username=username)
                posts = Post.objects.filter(author=profile)
            except Profile.DoesNotExist:
                return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            posts = Post.objects.all()

        search = request.GET.get('search')
        if search:
            posts = posts.filter(title__icontains=search)
        # order posts
        ordering = request.GET.get('ordering')
        if ordering:
            posts = posts.order_by(ordering)
        # paginate posts
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        # check if there is image in the request
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=Profile.objects.get(user=request.user))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def post(request, pk):
    if request.user.is_anonymous:
        return Response({'message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        # make sure that the user is the author of the post
        if post.author.user != request.user:
            return Response({'message': 'You are not the author of this post.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CreatePostSerializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'DELETE':
        # make sure that the user is the author of the post
        if post.author.user != request.user:
            return Response({'message': 'You are not the author of this post.'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({'message': 'Post deleted.'}, status=status.HTTP_204_NO_CONTENT)

