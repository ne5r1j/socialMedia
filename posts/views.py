from django.shortcuts import render
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from .models import Post
from users.models import Profile

# Create your views here.
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
    else:
        form = PostCreateForm(data=request.GET)
    return render(request, 'posts/create.html',{'form': form})


def feed(request):
    posts = Post.objects.all()
    return render(request, 'posts/feed.html', {'posts': posts})
