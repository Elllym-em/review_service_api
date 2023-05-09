from reviews.validators import validate_username
from rest_framework import serializers


from reviews.models import Category, Comment, Genre, Review, Title, User


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для проверки входящих данных при входе."""

    email = serializers.EmailField(max_length=254,)
    username = serializers.CharField(
        validators=[validate_username], max_length=150)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


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
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True,
    )

    class Meta:
        fields = '__all__'
        model = Title


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
