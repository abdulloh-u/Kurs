from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Kurs haqida to'liq")
    what_you_will_learn = models.TextField(verbose_name="Nimalar o'rgatilishi")
    duration = models.CharField(max_length=100, verbose_name="Davomiyligi (masalan: 3 oy)")
    level = models.CharField(max_length=50, verbose_name="O'qish darajasi (Boshlang'ich, O'rta)")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Narxi (so'm)")
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name="Kurs rasmi")
    is_active = models.BooleanField(default=True, verbose_name="Qabul ochiqmi?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title