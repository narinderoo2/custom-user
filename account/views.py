from django.shortcuts import render
from account.models import User,Post
from account.serializers import RegisterSerializer,PostSerializer

from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.decorators import api_view,APIView
from rest_framework.authtoken.models import Token

#permission allow
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication

#filter module import
from rest_framework.filters import SearchFilter,OrderingFilter

#pagination
from rest_framework.pagination import PageNumberPagination


@api_view(['POST',])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['Response'] = "Your account Register"
            data['username'] = account.username
            data['email'] = account.email
            data['password'] = account.password
            data['phone'] = account.phone
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


""" for admin 
            all user register get list"""

# @api_view(['GET',])
# def register_list(request):
#     try:
#         account = User.objects.all()
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = RegisterSerializer(account,many=True)
#         return Response(serializer.data)

# save the post with current user with token
class PostList(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def post(self,request):
        account = request.user
        add = Post(owner=account)
        serializer = PostSerializer(add,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# you can filter no. of post
class FilterList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,OrderingFilter)
    pagination_class = PageNumberPagination
    search_fields = ['body','title','owner__username']