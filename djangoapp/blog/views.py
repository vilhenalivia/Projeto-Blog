from django.shortcuts import render

#view INDEX
def index(request):
    return render(request,'blog/pages/index.html')
