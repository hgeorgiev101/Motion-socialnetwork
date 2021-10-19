from rest_framework import serializers
from post.models import Post
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked_by_me = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def get_is_liked_by_me(self, obj):
        if self.context['request'].user not in obj.liked_by.all():
            return False
        else:
            return True

    def get_image_url(self, obj):
        try:
            domain_name = 'https://motion-team-php.propulsion-learn.ch'
            full_path = domain_name + obj.images.url
            return full_path
        except:
            return None

    class Meta:
        model = Post
        fields = ['id', 'text_content', 'created', 'author', 'like_count', 'is_liked_by_me', 'images', 'external_link',
                  'shared_post', 'is_parent', 'image_url']
        read_only_fields = ['author']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author, many=False, context=self.context).data
        representation['images'] = representation.pop('image_url')
        if representation['shared_post'] is not None:
            shared_url = self.context['request'].build_absolute_uri()

            for i in range(len(shared_url)):  # this makes sure that the URL is correct going through multiple shares
                if shared_url[-1].isdigit() or shared_url[-1] == '/':
                    shared_url = shared_url[:-1]
                else:
                    break

            representation['shared_post'] = f"{shared_url}/{representation['shared_post']}"

        return representation
