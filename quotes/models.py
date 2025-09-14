from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Quote(models.Model):

    # Fields
    text = models.TextField(
        unique=True,
        verbose_name="Текст цитаты"
    )
    
    source = models.CharField(
        max_length=255,
        verbose_name="Источник"
    )

    weight = models.PositiveIntegerField(
        default=10,
        verbose_name="Вес (влияет на частоту показа)"
    )

    likes = models.PositiveIntegerField(
        default=0,
        verbose_name="Лайки"
    )

    dislikes = models.PositiveIntegerField(
        default=0,
        verbose_name="Дизлайки"
    )

    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Просмотры"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    # Methods
    # For admin panel
    def __str__(self):
        return f'"{self.text}" - {self.source}'


    # validation "no more than 3 quotes from one source"
    def clean(self):
        if self.pk is None:
            quote_count = Quote.objects.filter(source=self.source).count()
            if quote_count >= 3:
                raise ValidationError(f'Из источника "{self.source}" уже добавлено максимальное количество цитат (3)')


    # Meta class
    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"
        ordering = ['-created_at']  # Default sort in admin panel