from django.shortcuts import render
from django.contrib.auth.decorators import login_required # for Access Control

# Create your views here.
@login_required(login_url='login')
def index(request):
    context = {

    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='login')
def add_expense(request):
    context = {
        
    }
    return render(request, 'expenses/add_expense.html', context)
