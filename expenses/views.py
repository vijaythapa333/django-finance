from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # for Access Control
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


# Create your views here.
@login_required(login_url='login')
def index(request):
    owner = request.user
    expenses = Expense.objects.filter(owner=owner).order_by('-date')
    # For Pagination
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        owner = request.user

        category_obj = Category.objects.get(id=category)

        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, 'expenses/add_expense.html', context)
        
        # Save Expense to Datababse
        try:
            Expense.objects.create(amount=amount, description=description, category=category_obj, date=date, owner=owner)
            messages.success(request, "Expense Added.")
            return redirect('expenses')
        except:
            messages.error(request, "Failed to add Expense.")
            return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'categories': categories,
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)

    elif request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        # owner = request.user

        category_obj = Category.objects.get(id=category)

        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, 'expenses/edit_expense.html', context)
        
        # Save Expense to Datababse
        try:
            expense.amount=amount 
            expense.description=description
            expense.category=category_obj
            expense.date=date

            expense.save()
            
            messages.success(request, "Expense Updated Successfully.")
            return redirect('expenses')
        except:
            messages.error(request, "Failed to add Expense.")
            return render(request, 'expenses/edit_expense.html', context)


@login_required(login_url='login')
def delete_expense(request, id):
    expense_obj = Expense.objects.get(pk=id)

    try:
        expense_obj.delete()
        messages.success(request, "Expense Deleted.")
        return redirect('expenses')
    except:
        messages.error(request, "Failed to delete expense.")
        return redirect('expenses')


@login_required(login_url='login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__name__icontains=search_str, owner=request.user) # Extra Step for Foreign Key Category -> name

        data = expenses.values() # To pass all the values in the form of list
        
        return JsonResponse(list(data), safe=False)
