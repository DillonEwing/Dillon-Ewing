from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

from blog.models import Post, Comment
from blog.forms import CommentForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by('-created_on')
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, 'blog/category.html', context)


def blog_user_posts(request, username):
    """Show posts authored by a given user (by username)."""
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_on')
    context = {
        'user_profile': user,
        'posts': posts,
    }
    return render(request, 'blog/user_posts.html', context)


class SignUpView(FormView):
    """Simple signup view using Django's built-in UserCreationForm.

    On successful signup the user is automatically authenticated and logged in.
    """

    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = '/'  # redirect to home after signup

    def form_valid(self, form):
        # Save the new user
        user = form.save()
        # Authenticate and login the user
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def signup(request):
    """Function wrapper for the `SignUpView` to keep URL patterns simple.
    """
    view = SignUpView.as_view()
    return view(request)


class PostDetailView(FormMixin, DetailView):
    """Class-based view that shows a `Post` and handles posting comments.

    This replaces the previous function-based `blog_detail` view. It uses
    `DetailView` to provide the `post` object and `FormMixin` to render and
    validate `CommentForm`. On successful form submission it creates a
    `Comment` instance attached to the displayed post and redirects back to
    the same detail page.
    """

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        # Redirect back to the same post detail page after a successful POST
        return reverse('blog_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        # Add comments and the form to the template context
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        # Handle POST: bind the form and either save the comment or re-render
        # with validation errors.
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Create and save the comment. If the user is authenticated use their
        # username as the author; otherwise fall back to the form value.
        author_name = (
            self.request.user.username
            if self.request.user.is_authenticated
            else form.cleaned_data.get('author')
        )
        Comment.objects.create(
            author=author_name,
            body=form.cleaned_data['body'],
            post=self.object,
        )
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allow logged-in users to create new posts. The author is set to the
    current user automatically in form_valid.
    """

    model = Post
    fields = ['title', 'body', 'categories']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow the post owner to edit their post."""

    model = Post
    fields = ['title', 'body', 'categories']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # author should not change; keep existing
        return super().form_valid(form)

    def test_func(self):
        # Only allow the author to edit
        post = self.get_object()
        return self.request.user.is_authenticated and post.author == self.request.user

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow the post owner to delete their post."""

    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog_index')

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_authenticated and post.author == self.request.user


# For backwards-compatibility you can keep a tiny wrapper that uses the
# class-based view. This makes it safe to switch URLs immediately.
def blog_detail(request, pk):
    view = PostDetailView.as_view()
    return view(request, pk=pk)