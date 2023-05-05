from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnlyPermission,
                          IsAuthorAdminModeratorOrReadOnly, OnlyAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, JWTTokenSerializer,
                          ResponseSerializer, ReviewSerializer,
                          SignUpSerializer, TitleCreateSerializer,
                          TitleListSerializer, UserSerializer)
from .utils import generate_confirmation_code_and_send_email


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


@api_view(['POST'])
def signup_function(request):
    """Функция для регистрации нового пользователя"""

    data = request.data
    resp_ser = ResponseSerializer(data=data)
    resp_ser.is_valid(raise_exception=True)
    username = resp_ser.validated_data['username']
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        generate_confirmation_code_and_send_email(
            serializer.validated_data['username'],
            serializer.validated_data['email']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = get_object_or_404(User, username=username)
    serializer = SignUpSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['email'] == user.email:
        serializer.save()
        generate_confirmation_code_and_send_email(
            serializer.validated_data['username'],
            serializer.validated_data['email']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        'Вы неверно указали почту!',
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def token_function(request):
    """Функция для получения JWT-токена"""

    serializer = JWTTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    if (user.confirmation_code == serializer.validated_data['confirmation'
                                                            '_code']):
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        return Response({'token': access_token}, status=status.HTTP_200_OK)
    return Response(
        'Неверный код подтверждения!',
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения, обновления и удаления информации
    о пользователях"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (OnlyAdmin,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=username', )
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPostPatchDeleteViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.all().annotate(
            rating=Avg('reviews__score')
        )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleCreateSerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review. """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsAuthorAdminModeratorOrReadOnly, ]
        return super(ReviewViewSet, self).get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment. """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review())

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsAuthorAdminModeratorOrReadOnly, ]
        return super(CommentViewSet, self).get_permissions()
