from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models.query import QuerySet
from typing import Any

# Quantos itens por página
PER_PAGE = 9

class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    #lista de objetos
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    # Sobrescrevendo o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ 'page_title': 'Home - ' })
        return context

class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        ctx.update({
            'page_title': page_title,
        })

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        user = User.objects.filter(pk=author_id).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_id,
            'user': user,
        })

        return super().get(request, *args, **kwargs)

class CategoryListView(PostListView):
    # Erro 404 - Caso vazio
    allow_empty =  False

    # Query
    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get('slug'))
    
    # Contexto
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Categoria - '
        ctx.update({ 'page_title' : page_title })
        return ctx
    
class TagListView(PostListView):
    # Erro 404 - Caso vazio
    allow_empty =  False

    # Query
    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))
    
    # Contexto
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.firs().name} - Tag - '
        ctx.update({ 'page_title' : page_title })
        return ctx

class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({ 'page_title' : f'{search_value[:30]} - Search - ',  'search_value' : search_value, })
        return ctx

    # Redirect para buscas vazias 
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    #Onde buscar os dados da pagina
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page_title} - Página - '
        ctx.update({'page_title': page_title})
        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(is_published = True)


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

