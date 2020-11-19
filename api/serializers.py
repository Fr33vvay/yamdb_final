from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from content.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий
    """

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания произведений
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleListSerializer(serializers.ModelSerializer):
    """
    Сериализатор вывода списка произведений. Жанр и категорий используют
    собственные сериализаторы.
    """
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов на произведения.
    """
    author = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """
        Проверка, что отзыв ещё не оставлялся.
        """
        request = self.context.get('request')
        if request.method == 'POST':
            if Review.objects.filter(
                    title=self.context.get('view').kwargs.get('title_id'),
                    author=request.user,
            ).exists():
                raise ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )

        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор комментариев к отзывам.
    """
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class UsersSerializer(serializers.ModelSerializer):
    """
    Сераилизация работы с моделью User.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'bio',
                  'email', 'role',)
        extra_kwargs = {'username': {'required': True},
                        'email': {'required': True}
                        }


class UsersSerializerRoleReadOnly(UsersSerializer):
    role = serializers.CharField(read_only=True)


class EmailSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для генерации confirmation code.
    """
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email',)


class EmailCodeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для генерации token, при наличии confirmation code.
    """
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'confirmation_code',)
