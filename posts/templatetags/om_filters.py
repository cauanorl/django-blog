from django import template


register = template.Library()

@register.filter(name='plural_comments')
def plural_comments(num_comments):
    try:
        num_comments = int(num_comments)
        if num_comments == 0:
            return 'No Comments'
        elif num_comments == 1:
            return f'{num_comments} Comment.'
        else:
            return f'{num_comments} Comments.'
    except:
        return f'{num_comments} Comment(s)'


@register.filter('short')
def short_excerpt(excerpt):
    if len(excerpt) > 200:
        return f'{excerpt[:196]}...'
    return excerpt
