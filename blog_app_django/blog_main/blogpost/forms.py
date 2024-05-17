from django import forms
from .models import PostModel,Comments

class PostModelForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('title', 'content')

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('title', 'content')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('content',)
