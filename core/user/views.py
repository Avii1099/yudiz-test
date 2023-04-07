from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, AuthenticationFailed
from .models import UserBlog, User
from .serializers import BlogSerializers
from django.contrib.auth import authenticate
from rest_framework import status


class RegisterModelView(ModelViewSet):
    queryset = User.objects.all()
    http_method_allow = ["POST"]
    
    def create(self, request, *args, **kwargs):
        username = self.request.data.get("username")
        email = self.request.data.get("email")
        password = self.request.data.get("password")
        
        user, _ = User.objects.get_or_create(username=username, email=email)
        user.set_password(password)
        user.save()
        return Response(data=f"Create {user.username}")

class LoginViewSet(ModelViewSet):
    queryset = User.objects.all()
    http_method_allow = ["GET"]
    
    def get_queryset(self):
        username = self.request.GET.get("username")
        password = self.request.GET.get("password")
        
        user = self.queryset.filter(username=username).last()
        if not user:
            raise NotFound("Please provide correct username")
        
        user = authenticate(username=username, password=password)

        
        if not user:
            raise AuthenticationFailed()
        return user

    def list(self, request, *args, **kwargs):
        queryset_obj: User = self.filter_queryset(self.get_queryset())

        return Response(data={"message": f"login successfully {queryset_obj.username}"})

    
    

class ResetPasswordViewSet(ModelViewSet):
    queryset = User.objects.all()
    http_method_allow = ["POST"]
    
    def create(self, request, *args, **kwargs):
        username = self.request.data.get("username")
        password = self.request.data.get("password")
        
        user = self.queryset.filter(username=username).last()
        if not user:
            raise NotFound("Please provide correct username")
        
        user.set_password(password)
        user.save()
        return Response(data=f"Reset Password of {user.username}")
        


class BlogViewSet(ModelViewSet):
    queryset = UserBlog.objects.all()
    serializer_class = BlogSerializers
    
    def get_queryset(self):
        user_id = self.request.GET.get("user")
        user = User.objects.get(id=user_id)
        return self.queryset.filter(user = user)
    

    def create(self, request, *args, **kwargs):
        user_id = self.request.data.get("user")
        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

