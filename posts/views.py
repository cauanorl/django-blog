from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# https://docs.djangoproject.com/en/4.0/ref/class-based-views/
from django.views import View
from django.views.generic.list import ListView
# from django.views.generic.edit import UpdateView

""" Importes avançados envolvendo banco de dados """
from django.db.models import (
    Q, Count,
    Case, When
)

from django.db import connection

from .models import Post
from categories.models import Category
from comments.forms import CommentForm
from comments.models import Comment


# Create your views here.
class PostIndex(ListView):
    template_name = 'posts/index.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 6
    posts = Post.objects.all()

    extra_context = {
        'categories': Category.objects.all(),
    }

    def get_queryset(self):
        qs = super().get_queryset()
        self.extra_context.update({'category': self.kwargs.get('category')})
        qs = qs.select_related('category')
        qs = qs.order_by('-id').filter(
            published=True,
        ).annotate(
            len_comments=Count(  # faz um for nos models
                Case(  # Faz um if dentro do for Count
                    When(
                        comment__published_comment=True,
                        then=1  # Caso a condição seja True
                        ))))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connection'] = connection
        return context


class PostSearch(PostIndex):
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('termo')

        if not term:
            return qs

        qs = qs.filter(
            Q(title__icontains=term) | Q(author__username__iexact=term) |
            Q(content__icontains=term) | Q(excerpt__icontains=term) |
            Q(category__category_name__icontains=term),
        )

        return qs


class PostCategory(PostIndex):
    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('category', None)
        self.extra_context.update({"category": f"- {category}"})

        if not category:
            return qs

        return qs.filter(
            category__category_name__iexact=category,
        )


class PostDetails(View):
    template_name = 'posts/post_details.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        pk = self.kwargs.get('pk')
        self.context = {
            'post': get_object_or_404(Post, pk=pk, published=True),
            'comments': Comment.objects.filter(
                published_comment=True,
                post_comment=pk,
            ),
            'form': CommentForm(request.POST or None),
            'categories': Category.objects.all(),
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.context['form']
        if not form.is_valid() or not request.user.is_authenticated:
            return render(request, self.template_name, self.context)

        form = form.save(commit=False)
        form.user_comment = request.user
        form.email_comment = request.user.email
        form.post_comment = self.context['post']
        form.save()
        messages.success(request, 'Comentado')

        return redirect('post_details', pk=self.kwargs.get('pk'))


# class PostDetails(UpdateView):
#     template_name = 'posts/post_details.html'
#     model = Post
#     context_object_name = 'post'
#     form_class = CommentForm
#     extra_context = {
#         'categories': Category.objects.all(),
#     }

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         comments = Comment.objects.filter(
#             published_comment=True,
#             post_comment=post.id,
#         )
#         context['comments'] = comments

#         return context

#     def form_valid(self, form):
#         post = self.get_object()
#         comment = Comment(**form.cleaned_data)
#         comment.post_comment = post

#         if self.request.user.is_authenticated:
#             comment.user_comment = self.request.user

#         comment.save()
#         return redirect('post_details', pk=post.id)
