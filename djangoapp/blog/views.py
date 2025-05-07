from django.core.paginator import Paginator
from django.shortcuts import render

posts = list(range(1000))

#view INDEX
def index(request):
    paginator = Paginator(posts,9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 'page_obj': page_obj, } 

    return render(request,'blog/pages/index.html', context)

def page(request):
    paginator = Paginator(posts,9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 'page_obj': page_obj, }

    return render(request,'blog/pages/page.html', context)

def post(request):
    paginator = Paginator(posts,9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={ 'page_obj': page_obj, }
    return render(request,'blog/pages/post.html', context)
