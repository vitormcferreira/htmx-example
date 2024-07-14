import random
from http import HTTPStatus
from time import sleep

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from . import forms, models


@require_http_methods(['GET'])
def news_list(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', 1)
    search = request.GET.get('search')

    qs = models.News.objects.all()

    if search is not None:
        qs = qs.filter(Q(title__icontains=search) | Q(subtitle__icontains=search))

    news_list = Paginator(qs.order_by('-id'), 6, 5).page(page)

    if request.headers.get('HX-Trigger') in ['paginator', 'search']:
        template_name = 'news/includes/news_cards.html'
    else:
        template_name = 'news/news_list.html'

    return render(request, template_name, {'news_list': news_list})


@require_http_methods(['GET'])
def comments_count_field(request: HttpRequest, pk) -> HttpResponse:
    sleep(random.randint(0, 3))
    comments_count = random.randint(0, 5)
    return render(
        request,
        'news/includes/comments_count_field.html',
        {'comments_count': comments_count},
    )


@require_http_methods(['GET'])
def more(request: HttpRequest, pk) -> HttpResponse:
    news = models.News.objects.get(pk=pk)
    sleep(random.randint(0, 2))
    if random.randint(0, 1):
        messages.error(request, 'Error while fetching.')
        return render(
            request,
            'news/fragments/more_500.html',
            {'news': news},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    return render(request, 'news/fragments/more.html', {'news': news})


@require_http_methods(['GET', 'POST'])
def news_create(request: HttpRequest) -> HttpResponse:
    form = forms.NewsForm(request.POST or None)

    if request.method == 'GET':
        return render(request, 'news/news_create.html', {'form': form})

    if not form.is_valid():
        messages.error(request, 'Error on create news.')
        response = render(request, 'news/news_create.html', {'form': form})
        response['HX-Push-Url'] = 'false'
        return response

    messages.success(request, 'News created with success')
    form.save()
    return redirect('news:news_list')


@require_http_methods(['GET', 'POST'])
def news_edit(request: HttpRequest, pk) -> HttpResponse:
    news = models.News.objects.get(pk=pk)
    form = forms.NewsForm(request.POST or None, instance=news)

    if request.method == 'GET':
        return render(request, 'news/news_edit.html', {'form': form})

    if not form.is_valid():
        messages.error(request, 'Error on update news.')
        response = render(request, 'news/news_edit.html', {'form': form})
        response['HX-Push-Url'] = 'false'
        return response

    messages.success(request, 'News updated with success.')
    form.save()
    return redirect('news:news_list')


@require_http_methods(['DELETE'])
def news_delete(request: HttpRequest, pk) -> HttpResponse:
    models.News.objects.filter(pk=pk).delete()
    messages.success(request, 'News removed with success')
    return render(request, 'fragments/messages.html')
