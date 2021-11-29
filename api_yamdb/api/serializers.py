from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate(self, data):
        request = self.context['request']
        username = request.query_params.get('username')
        user = request.user
        if not (
            user.is_admin() or username == user.username
            or request.path == reverse('users-me')
        ):
            raise serializers.ValidationError(
                'Нельзя менять другого пользователя'
            )
        if 'role' in data:
            if user.is_admin():
                return data
            data['role'] = User.USER_ROLE
            return data
        return data


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.save()
        return user

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя не может быть me')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        read_only=True,
        required=False,
        min_value=1,
        max_value=10
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        many=True, queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        request = self.context['request']
        if request.method == 'POST' and Review.objects.filter(
                title=title, author=request.user).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date', ]
        model = Comment


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    confirmation_code = serializers.CharField(max_length=150)
