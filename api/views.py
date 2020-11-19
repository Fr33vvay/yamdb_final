from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from content.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .permissions import (IsAdminModeratorOrAuthorOrReadOnly,
                          IsAdminOrReadOnly,
                          IsAdministrator)
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailCodeSerializer, EmailSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UsersSerializer, UsersSerializerRoleReadOnly)


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Вьюсет, обесечивающий дефолтные `create()`, `destroy()`, `list()`.
    """
    pass


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Вьюсет жанров.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    permission_classes = [IsAdminOrReadOnly, ]

    search_fields = ['=name', ]
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Вьюсет категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrReadOnly, ]

    search_fields = ['=name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет произведений.
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))

    permission_classes = [IsAdminOrReadOnly, ]

    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет отзывов на произведения.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOrAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет комментариев к отзывам.
    """
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOrAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title_id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title_id=self.kwargs.get('title_id'))
        serializer.save(review=review, author=self.request.user)


def send_service_mail(mail_to: str, message: str,
                      subject: str = None):
    """
    Обеспечивает отправку электронного сообщения.
    Заголовок (subject) предустановлен.
    :param mail_to: Электронный адрес.
    :param message: Текст сообщения.
    :param subject: Тема сообщения (если None используется default).
    """

    subject = subject or settings.DEFAULT_EMAIL_SUBJECT

    send_mail(subject=subject,
              message=message,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[mail_to],
              fail_silently=True
              )


class EmailAuthenticatedSet(viewsets.ViewSet):
    """
    Авторизация и получение токена в обмен на confirmation code,
    полученный на электронную почту.
    """

    @action(detail=False, methods=['post'], url_path='email')
    def get_confirmation_code(self, request):
        """
        Отправление confirmation_code на переданный email.
        """
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, create = User.objects.get_or_create(
            email=serializer.data.get('email')
        )
        if create:
            user.username = serializer.data.get('email')
            user.save()

        code = default_token_generator.make_token(user)
        send_service_mail(user.email, code)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='token')
    def get_token(self, request):
        """
        Получение JWT-токена в обмен на email и confirmation_code.
        """
        serializer = EmailCodeSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, email=serializer.validated_data.get('email')
        )

        code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, code):
            refresh = RefreshToken.for_user(user)
            user.is_active = True
            return Response({'token': f'{refresh.access_token}'},
                            status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Работа с пользователями (User): создание, редактирование, удаление.
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated,
                          IsAdministrator, ]

    filter_backends = (filters.SearchFilter,)
    search_fields = ['username']

    lookup_field = 'username'

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated, ],
            url_path='me')
    def my_user_object(self, request):
        serializers = UsersSerializer(self.request.user)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @my_user_object.mapping.patch
    def upd_me(self, request):
        serializers = UsersSerializerRoleReadOnly(self.request.user,
                                                  data=self.request.data,
                                                  partial=True)

        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
