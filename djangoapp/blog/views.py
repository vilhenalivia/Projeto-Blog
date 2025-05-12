from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView

# Quantos itens por página
PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    #lista de objetos
    context_object_name = 'page_obj'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset
     
    # Sobrescrevendo o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'page_title': 'Home - ' })
        return context
    


#view INDEX
def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 
        'page_obj': page_obj, 
        'page_title': 'Home - ',
    } 

    return render(request,'blog/pages/index.html', context)

# view PAGE
def page(request, slug):
    page = Page.objects.filter(is_published = True).filter(slug=slug).first()
    
    if page is None:
        raise Http404 
    
    page_title = f'{page.title} - Página - '

    context = {
        'page' : page ,
        'page_title': page_title,
    }
    return render(request,'blog/pages/page.html',context)

# view POST
def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first()
    if post is None:
        raise Http404 
    
    page_title = f'{post.title} - Post - '
    context = {
        'post' : post,
        'page_title': page_title,
    }
    return render(request,'blog/pages/post.html', context)

#view INDEX
def created_by(request, author_id):
    user = User.objects.filter(pk=author_id).first()

    if user is None:
        raise Http404()

    posts = Post.objects.get_published().filter(created_by__pk=author_id)
    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user_full_name} {user.last_name}'
    
    page_title = "Post de" + user_full_name + '-'

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 
        'page_obj': page_obj, 
        'page_title': page_title,
    } 

    return render(request,'blog/pages/index.html', context)

#view CATEGORIA
def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug =slug)

    if len(posts) ==  0:
        raise Http404

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    page_title = f'{page_obj[0].category.name} - Categoria - '

    context ={ 
        'page_obj': page_obj, 
        'page_title': page_title,
    } 

    return render(request,'blog/pages/index.html', context)

#view TAGS
def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug =slug)

    if len(posts) ==  0:
        raise Http404 
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_title = f'{page_obj[0].tags.first().name} - Tag - '
    context ={ 
        'page_obj': page_obj, 
        'page_title': page_title,
    } 

    return render(request,'blog/pages/index.html', context)

#view SEARCH
def search(request):
    search_value = request.GET.get('search', '' ).strip()
    posts = Post.objects.get_published().filter(
        Q( title__icontains= search_value ) |
        Q( excerpt__icontains= search_value ) |
        Q( content__icontains= search_value ) 
    )[0:PER_PAGE]

    if len(posts) ==  0:
        raise Http404 
    
    page_title = f'{search_value[:30]} - Search - '
    context = {
        'page_obj' : posts ,
        'search_value' : search_value,
        'page_title': page_title,
    }

    return render(request,'blog/pages/index.html', context)
