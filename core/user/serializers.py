from rest_framework import serializers
from .models import UserBlog
from django.utils import timezone
class BlogSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = UserBlog
        fields = ("title", "blog", "user")
        read_only_fields = ("user",)
    
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        title = validated_data.get("title")
        blog = validated_data.get("blog")
        user = self.context.get("user")
        print('user: ', user)
        user_blog = UserBlog.objects.create(user=user, title=title, blog=blog, create_at=timezone.now())
        return user_blog