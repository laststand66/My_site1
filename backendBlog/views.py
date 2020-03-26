from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import generic
from .models import Article, MainUser, Comment, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages

from .forms import ChangeUserInfoForm, RegisterUserForm, CommentForm
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView


#home page
def index(request):
    return render(request, 'basic.html')

#login page
class BlogLoginView(LoginView):
    template_name = 'backendBlog/login.html'


# class ArticleList(generic.ListView):
#
#     expression = '-pub_date'
#     queryset = Article.objects.filter(status=1).order_by(expression)
#     template_name = 'backendBlog/article_list.html'



#view for articles on frontpage and on sidebar (remake after class view)
def article_list(request):
    expression = '-pub_date'
    article_list = Article.objects.filter(status=1).order_by(expression)

    sidebar_list_recent = Article.objects.filter(status=1).order_by(expression)[:5]
    sidebar_list_popular = Article.objects.filter(status=1).order_by('-likes')[:5]

    context = {
        'article_list': article_list,
        'sidebar_list_popular': sidebar_list_popular,
        'sidebar_list_recent': sidebar_list_recent,
    }
    return render(request, 'backendBlog/article_list.html', context)


# class ArticleDetail(generic.DetailView):
#     model = Article
#     template_name = 'backendBlog/article_detail.html'

#view for article pages (remake after class view)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    is_liked = False
    if article.likes.filter(id=request.user.id).exists():
        is_liked = True
    is_favorite = False
    if article.favorite.filter(id=request.user.id).exists():
        is_favorite = True
    context = {
    'article': article,
    'is_liked': is_liked,
    'is_favorite': is_favorite,
    'total_likes': article.total_likes()
    }
    return render(request, 'backendBlog/article_detail.html', context)




@login_required
def profile(request):
    return render(request, 'backendBlog/profile_tmp/profile.html')

# class for profile logout
class BlogLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'backendBlog/profile_tmp/logout.html'



# class for changing user info
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = MainUser
    template_name = 'backendBlog/profile_tmp/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('backendBlog:profile')
    success_message = 'User info was changed'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


#class for changing passwor
class MainPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'backendBlog/profile_tmp/password_change.html'
    success_url = reverse_lazy('backendBlog:profile')
    success_message = 'Пароль успешно изменен'


#class for user registration
class RegisterUserView(CreateView):
    model = MainUser
    template_name = 'backendBlog/profile_tmp/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('backendBlog:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'backendBlog/profile_tmp/register_done.html'


#class for deleting user by himself
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = MainUser
    template_name = 'backendBlog/profile_tmp/delete_user.html'
    success_url = reverse_lazy('backendBlog:home')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# views for likes in article

def like_article(request):
    article = get_object_or_404(Article, id=request.POST.get('article_id'))
    is_liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        is_liked = False
    else:
        article.likes.add(request.user)
        is_liked = True
    return redirect('backendBlog:article_detail', slug=article.slug)


# views for adding articles to favorite (same as likes tho)
def add_favorite(request):
    article = get_object_or_404(Article, id=request.POST.get('article_id'))
    is_favorite = False
    if article.favorite.filter(id=request.user.id).exists():
        article.favorite.remove(request.user)
        is_favorite = False
    else:
        article.favorite.add(request.user)
        is_favorite = True
    return redirect('backendBlog:article_detail', slug=article.slug)


#list of categories (no links set on templates)
def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'backendBlog/categories_list.html', context={'categories' : categories})


# addig coments by users
def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.name = request.user
            form.article = article
            form.save()

            return redirect('backendBlog:article_detail', slug=article.slug)
    else:
        form = CommentForm()
    template = 'backendBlog/add_comment.html'
    context = {'article': article, 'form':form, }
    return render(request, template, context)
