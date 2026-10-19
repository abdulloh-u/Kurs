from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Tavsif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    duration = models.CharField(max_length=50, default="3 oy", verbose_name="Davomiyligi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlandi'),
        ('rejected', 'Rad etildi'),
    )

    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqam")
    age = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(36)],
        verbose_name="Yosh (10-36)"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Tanlangan kurs")
    note = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha izoh")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holati")
    chat_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telegram Chat ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.course.title}"
