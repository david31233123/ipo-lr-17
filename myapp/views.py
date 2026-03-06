from django.shortcuts import render
def home(request):
    return render(request, 'home.html')

def author(request):
    return render(request, 'author.html')

def shop(request):
    return render(request, 'shop.html')