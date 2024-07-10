from django.db import models


class AuthUser(models.Model):
    """ Модель пользователя на платформе
    """
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)

    @property
    def is_authenticated(self):
        """ Всегда возвращает True. Это способ узнать, был ли пользователь аутентифицированы
        """
        return True

    def __str__(self):
        return self.email
