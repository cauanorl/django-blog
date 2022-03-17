from django.forms import ModelForm
from .models import Comment
from django.contrib import messages


class CommentForm(ModelForm):
    def clean(self):
        data = self.cleaned_data
        name = data.get('name_comment')
        comment = data.get('comment')

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

