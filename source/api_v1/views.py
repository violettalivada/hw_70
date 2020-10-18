import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie

from api_v1.serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return JsonResponse(slr.data, safe=False)


class ArticleCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slr = ArticleSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response


class ArticleView(APIView):
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs.keys():
            article = get_object_or_404(Article, pk=kwargs.get('pk'))
            slr = ArticleSerializer(article)
            return Response(slr.data)

    def put(self, request, pk):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        data = request.data.get('article')
        srl = ArticleSerializer(instance=article, data=data, partial=True)
        if srl.is_valid(raise_exception=True):
            article = srl.save()
        return Response({
            "success": "Article '{}' updated successfully".format(article.title)
        })

    def delete(self, request, pk):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)



