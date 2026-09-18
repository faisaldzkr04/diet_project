from django import forms
from .models import Food

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'carbs', 'protein', 'fat', 'fiber', 'sodium']