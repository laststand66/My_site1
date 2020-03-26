from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

# from . import views

app_name = 'backendBlog'


urlpatterns = [
    path('categories/', categories_list, name='categories_list_url'),
    path('favorite/', add_favorite, name='add_favorite'),
    path('like/', like_article, name='like_article'),
    path('<str:slug>/comment/', add_comment, name='add_comment'),

    path('accounts/profile/delete', DeleteUserView.as_view(), name='profile_delete'),

    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/password/change/', MainPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/change', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/logout/', BlogLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('<str:slug>/', article_detail, name='article_detail'),
    path('accounts/login/', BlogLoginView.as_view(), name='login'),

    path('', article_list, name='home'),

    # path('', ArticleList.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
