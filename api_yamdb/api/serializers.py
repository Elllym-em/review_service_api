import datetime as dt

from django.core.validators import RegexValidator
from rest_framework import serializers, status
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if (data.get('username') is not None
                and data.get('username').lower() == 'me'):
            raise serializers.ValidationError(
                'Username должен иметь отличное значение от "me"'
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Неккоректно введён <username>',
            code='invalid_username'
        )
    ],
        max_length=150
    )

    def validate_username(self, value):
        if value is None:
            return Response({'username': 'Это поле не может быть пустым.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif value.lower() == 'me':
            raise serializers.ValidationError('Username cannot be "me"')
        return value

    class Meta:
        model = User
        fields = ('email', 'username')


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        fields = [
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        ]
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            author=self.context['request'].user,
            title=self.context.get('view').kwargs.get('title_id')
        ).exists():
            raise serializers.ValidationError('Отзыв уже создан')
        return data

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date', ]
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date', ]
        model = Comment


class ResponseSerializer(serializers.Serializer):
    """Сериализатор для проверки входящих данных."""

    username = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Неккоректно введён <username>',
            code='invalid_username'
        )
    ],
        max_length=150
    )
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value is None:
            return Response({'username': 'Это поле не может быть пустым.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif value.lower() == 'me':
            raise serializers.ValidationError('Username cannot be "me"')
        return value
