from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse
from .models import Review, Comment
from .forms import ReviewForm, CommentForm


@require_GET
def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'community/index.html', context)


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@require_GET
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)


@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_liked = False
        else:
            review.like_users.add(user)
            is_liked = True
        context = {
            'is_liked' : is_liked,
            'count' : review.like_users.count()
        }
        return JsonResponse(context)
    return redirect('accounts:login')

@require_POST
def comment_like(request, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        user = request.user

        if comment.commentlike_users.filter(pk=user.pk).exists():
            comment.commentlike_users.remove(user)
            is_commentliked = False

        else:
            comment.commentlike_users.add(user)
            is_commentliked = True

        context = {
            'is_commentliked' : is_commentliked,
            'count' : comment.commentlike_users.count()

        }
        return JsonResponse(context)

@require_POST
def second_comment(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        secondcomment = comment_form.save(commit=False)
        secondcomment.origin_comment = comment
        secondcomment.user = request.user
        secondcomment.save()
        return redirect('community:detail', comment.pk)
    context = {
        'comment_form': comment_form,
        'comment' : comment,
        'secondcomments' : comment.second_comment.all(),
    } #related name을 썼으니, set 필요없음
    return render(request, 'community/detail.html', context)
