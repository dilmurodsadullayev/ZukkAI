from django import forms
from django.contrib.auth.models import User
from .models import Profile, Feedback


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone_number', 'school', 'grade', 'bio']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message', 'rating']
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': 'Xabar mavzusi...',
                'class': 'w-full p-4 rounded-xl bg-slate-50 border-2 border-transparent focus:border-indigo-500 outline-none transition font-medium'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Fikringizni shu yerga yozing...',
                'rows': 5,
                'class': 'w-full p-4 rounded-xl bg-slate-50 border-2 border-transparent focus:border-indigo-500 outline-none transition font-medium'
            }),
            'rating': forms.Select(choices=[(i, f"{i} yulduz") for i in range(5, 0, -1)], attrs={
                'class': 'w-full p-4 rounded-xl bg-slate-50 border-2 border-transparent focus:border-indigo-500 outline-none transition font-bold text-indigo-600'
            }),
        }