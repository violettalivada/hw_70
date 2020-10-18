from django.urls import path

from api_v1.views import get_token_view, ArticleListView, ArticleCreateView, ArticleView

app_name = 'api_v1'

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', ArticleView.as_view())
]
