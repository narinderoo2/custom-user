from rest_framework import serializers
from account.models import User,Post

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password','phone')


# Model of Post use

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_owner')

    class Meta:
        model = Post
        fields =('title','body','username','create_at')

    def get_username_from_owner(self,post):
        name = post.owner.username
        return name