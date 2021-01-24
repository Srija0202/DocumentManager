from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from .models import *
from django.db.models import Q


# Create your views here.


def index(request):
    url = '/login'
    if request.user.is_authenticated:
        url = '/dashboard'

    return redirect(url)


def dashboard(request):
    context = {'user': request.user, 'menu': 'dashboard'}
    document_count = Document.objects.count()
    document_type_count = DocumentType.objects.count()
    context.update(document_count=document_count, document_type_count=document_type_count)
    return render(request, 'dashboard.html', context)


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid Credentials'})   
    

def logout_user(request):
    logout(request)
    return redirect('/login')



def document(request):
    if request.method == 'GET':
        documents = Document.objects.values('id','name','document_type__name')
        return render(request, 'document.html', {'documents': documents, 'list':True, 'menu': 'document'})
    else:
        query = request.POST.get('query', '')
        documents = Document.objects.filter(Q(ocr_data__contains=query) | Q(name__contains=query)).values('id','name','document_type__name')
        message = '{} Document(s) found containing the name or keyword in the content "{}"'.format(len(documents), query)
        return render(request, 'document.html', {'documents': documents, 'list':True, 'menu': 'document', 'message':message})
    


def document_add(request):
    if request.method=='GET':
        types = DocumentType.objects.values('id', 'name')
        return render(request, 'document.html', {'types': types, 'list':False, 'menu': 'document'})
    else:
        name = request.POST.get('name')
        doc_type = request.POST.get('type')
        doc = request.FILES.get('document')
        print(request.FILES, request.POST)
        fs = FileSystemStorage() 
        file = fs.save(doc.name, doc) 
        doc = Document(name=name, document_type_id=int(doc_type), document=file)
        doc.save()
        return redirect('/document/{}/'.format(doc.id))


def document_edit(request, id):
    try:
        document = Document.objects.get(pk=id)
    except:
        return render(request, 'document.html', {'error_message':'No Document found for the ID %s' % id, 'list':False, 'menu': 'document'})        

    if request.method == 'GET':
        types = DocumentType.objects.values('id', 'name')
        context = {'types': types, 'list':False, 'menu': 'document'}
        context.update(id=document.id,name=document.name, type=document.document_type.name, selected_file=document.document.name)
        return render(request, 'document.html', context)
    else:
        document.name = request.POST.get('name')
        document.document_type_id = int(request.POST.get('type'))
        doc = request.FILES.get('document')
        if doc:
            fs = FileSystemStorage() 
            file = fs.save(doc.name, doc) 
            document.document = file
        document.save()            

    return redirect('/document/{}/'.format(id))


def document_delete(request, id):
    try:
        document = Document.objects.get(pk=id)
    except:
        return HttpResponse('No document Found for the id %s' % id)
    document.delete()

    return redirect('/document')