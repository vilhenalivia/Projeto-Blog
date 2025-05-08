from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post

PER_PAGE = 9

#view INDEX
def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-id')

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 'page_obj': page_obj, } 

    return render(request,'blog/pages/index.html', context)

def page(request):
    return render(request,'blog/pages/page.html',)

def post(request):
    return render(request,'blog/pages/post.html',)
