from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'phone', 'age', 'course', 'note']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'phone': 'Telefon raqam',
            'age': 'Yosh (10-36)',
            'course': 'Tanlangan kurs',
            'note': "Qo'shimcha izoh",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ali'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valiyev'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 18', 'min': 10, 'max': 36}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "Savollaringiz yoki qo'shimcha istaklaringiz bo'lsa yozib qoldiring..."}),
        }