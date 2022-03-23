from django import forms

from .models import WebcamPic

class WebcamPicForm(forms.ModelForm):
    class Meta:
        model = WebcamPic
        fields = [
            'title',
            # 'screenshot'
        ]