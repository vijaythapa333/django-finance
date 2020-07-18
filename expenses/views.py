from django.shortcuts import render

# Create your views here.

def index(request):
    context = {

    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    context = {
        
    }
    return render(request, 'expenses/add_expense.html', context)
