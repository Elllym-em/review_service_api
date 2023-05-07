from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    first_name = models.TextField(
        max_length=150,
        blank=True
    )
    last_name = models.TextField(
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Статус пользователя',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=150,
        null=True,
        default=None
    )

    class Meta:
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(fields=('username', 'email'),
                                    name='unique_username&email')
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
    )
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    text = models.TextField()

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', ],
                name='Anti-abuse constraint: one review for one title'
            )
        ]

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField()

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
