from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_safe
from .models import Movie, Genre
from django.contrib.auth import get_user_model
from django.db.models import Max
import random


# Create your views here.
@require_safe
def index(request):
    movies = get_list_or_404(Movie)
    context = {
        'movies': movies, 
    }
    return render(request, 'movies/index.html', context)

@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk) # 선택한 movie 정보 받아오기 
    genres = movie.genres.all()                   # 해당 movie에 대한 genre 전체 리스트 받아오기

    context = {
        'movie' : movie,
        'genres' : genres,
    }
    return render(request, 'movies/detail.html', context)

@require_safe
def recommended(request):
    if request.user.is_authenticated:
        max_id = Movie.objects.all().aggregate(max_id = Max("id"))['max_id']
        movies = []
        cnt = 0
        while True:
            cnt += 1
            pk = random.randint(1, max_id)
            movie = Movie.objects.get(pk=pk)
            movies.append(movie)
            if cnt == 10:
                break

    context = {
        'movies': movies
    }

    return render(request, 'movies/recommended.html', context)