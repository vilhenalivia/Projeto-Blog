from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post

PER_PAGE = 9

#view INDEX
def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 'page_obj': page_obj, } 

    return render(request,'blog/pages/index.html', context)

# view PAGINA
def page(request, slug):
    return render(request,'blog/pages/page.html',)

# view POST
def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first()
    context = {'post' : post }
    return render(request,'blog/pages/post.html', context)

#view INDEX
def created_by(request, author_id):
    posts = Post.objects.get_published().filter(created_by__pk=author_id)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 'page_obj': page_obj, } 

    return render(request,'blog/pages/index.html', context)

#view CATEGORIA
def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug =slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 'page_obj': page_obj, } 

    return render(request,'blog/pages/index.html', context)