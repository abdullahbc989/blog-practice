from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comment

from posts.models import Post

detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug',
    )


class PostListSerializer(ModelSerializer):
    url = detail_url
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'id',
            'title',
            'publish',
        ]


class PostDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'user',
            'id',
            'title',
            'image',
            'slug',
            'content',
            'html',
            'publish',
            'comments',
        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_html(self, obj):
        return obj.get_markdown()

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
        ]

"""
data = {
    "title": "Yeahh buddy",
    "content": "New content",
    "publish": "2016-2-12",
    "slug": "yeah-buddy",
}

new_item = PostSerializer(data=data)
if new_item.is_valid():
    new_item.save()
else:
    print(new_item.errors)
"""
