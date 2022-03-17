from django.forms import ModelForm
from .models import Comment

import requests


class CommentForm(ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name_comment')
        comment = cleaned_data.get('comment')

        g_recaptcha_response = self.data.get('g-recaptcha-response')
        secret_recaptcha_key = '6Le4geseAAAAAPNb9nckCONXQHCnuUTJNPhvonCt'

        # https://www.google.com/recaptcha/api/siteverify
        recaptcha_request = requests.post(
            url='https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': secret_recaptcha_key,
                'response': g_recaptcha_response,
            },
        )

        recaptcha_result = recaptcha_request.json()

        if not recaptcha_result.get('success'):
            self.add_error(
                'comment',
                'Please check the "I am not a robot" box.',
            )

        if not name:
            self.add_error(
                'name_comment',
                'The name cannot be blank.'
            )

        if len(name) < 5:
            self.add_error(
                'name_comment',
                'Name cannot be less than 5 characters.'
            )
        
        if not comment:
            self.add_error(
                'comment',
                'The comment cannot be blank'
            )
        
        if len(comment) < 5:
            self.add_error(
                'comment',
                'The comment cannot be less then 5 characters.',
            )

    class Meta:
        model = Comment
        fields = ('name_comment', 'comment')

