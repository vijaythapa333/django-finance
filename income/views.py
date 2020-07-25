from django.shortcuts import render, redirect
from .models import Income, Source
from userpreferences.models import UserPreference
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required # for Access Control
from django.contrib import messages
import json
from django.http import JsonResponse

# Create your views here.

def index(request):
    owner = request.user
    incomes = Income.objects.filter(owner=owner).order_by('-date')

    # For Pagination
    paginator = Paginator(incomes, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    # Sending User Preference also
    user_preference = UserPreference.objects.get(user=owner)

    context = {
        'incomes': incomes,
        'page_obj': page_obj,
        'user_preference': user_preference,
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST,
    }

    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        owner = request.user

        source_obj = Source.objects.get(id=source)

        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, 'income/add_income.html', context)
        
        # Save Expense to Datababse
        try:
            Income.objects.create(amount=amount, description=description, source=source_obj, date=date, owner=owner)
            messages.success(request, "Income Added.")
            return redirect('incomes')
        except:
            messages.error(request, "Failed to add Income.")
            return render(request, 'income/add_income.html', context)


@login_required(login_url='login')
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'sources': sources,
    }

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)

    elif request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        # owner = request.user

        source_obj = Source.objects.get(id=source)

        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, 'income/edit_income.html', context)
        
        # Save income to Datababse
        try:
            income.amount=amount 
            income.description=description
            income.source=source_obj
            income.date=date

            income.save()
            
            messages.success(request, "Income Updated Successfully.")
            return redirect('incomes')
        except:
            messages.error(request, "Failed to add Income.")
            return render(request, 'income/edit_income.html', context)



@login_required(login_url='login')
def delete_income(request, id):
    income_obj = Income.objects.get(pk=id)

    try:
        income_obj.delete()
        messages.success(request, "Income Deleted.")
        return redirect('incomes')
    except:
        messages.error(request, "Failed to delete income.")
        return redirect('incomes')


@login_required(login_url='login')
def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__name__icontains=search_str, owner=request.user) # Extra Step for Foreign Key Category -> name

        data = incomes.values() # To pass all the values in the form of list
        
        return JsonResponse(list(data), safe=False)