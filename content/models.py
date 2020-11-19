from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from content.validators import validate_year

User = get_user_model()


class Category(models.Model):
    """
    Категории произведений, к которым пишутся отзывы (фильм,
    песня, спектакль).
    """
    name = models.CharField(verbose_name='Категория', max_length=30,
                            unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """
    Жанры произведений, к которым пишутся отзывы (комедия,
    хоррор, рок, поп).
    """
    name = models.CharField(verbose_name='Жанр', max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм,
    книга или песенка).
    """
    name = models.CharField(verbose_name='Произведение', max_length=200)
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='title')
    genre = models.ManyToManyField(Genre, blank=True, related_name='title')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """
    Отзывы на произведения.
    """
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(User, verbose_name='Автор',
                               related_name='reviews',
                               on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(verbose_name='Оценка',
                                             validators=[
                                                 MaxValueValidator(10),
                                                 MinValueValidator(1)
                                             ])
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True, db_index=True)
    title = models.ForeignKey(Title, verbose_name='Произведение',
                              related_name='reviews',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} - {self.title}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """
    Комментарии к отзывам.
    """
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(User, verbose_name='Автор',
                               related_name='comments',
                               on_delete=models.CASCADE)
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True, db_index=True)
    review = models.ForeignKey(Review, verbose_name='Отзыв',
                               related_name='comments',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} - {self.review}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
