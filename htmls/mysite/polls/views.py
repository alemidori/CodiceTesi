from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadFile
from django.http import HttpResponseRedirect
import sys
sys.path.append('/Users/Alessandra/Desktop/PycharmProjects/progetto_inforet')
import main


def welcome(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['name_file'])
            handle_uploaded_file(request.FILES['name_file'], str(request.FILES['name_file']))
            main.main('textfiles/' + str(request.FILES['name_file']))
            return HttpResponseRedirect('/index/')
    else:
        form = UploadFileForm()
        return render(request, "welcome.html" , {'form': form})

def index(request):
    return render(request, 'index.html')

def topic(request):
    return render(request, "topic.html")


def handle_uploaded_file(f,name):
    with open('textfiles/' + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)






