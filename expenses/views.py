from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # for Access Control
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import csv
import xlwt

#importing for pdf
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
from django.db.models import Sum


# Create your views here.
@login_required(login_url='login')
def index(request):
    owner = request.user
    expenses = Expense.objects.filter(owner=owner).order_by('-date')
    # For Pagination
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    # Sending User Preference also
    user_preference = UserPreference.objects.get(user=request.user)

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'user_preference': user_preference,
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


@login_required(login_url='login')
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)

    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)

    final_data = {}

    def get_category(expense):
        return expense.category.id
    category_list = list(set(map(get_category, expenses)))


    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount


    for x in expenses:
        for y in category_list:
            final_data[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data':final_data}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')



def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+ str(datetime.datetime.now()) +'.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date']) # File Header

    expenses = Expense.objects.filter(owner=request.user)
    # Data from Database
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category.name, expense.date])
    
    return response


def export_excel(requet):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+ str(datetime.datetime.now()) +'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']

    # For Header
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=requet.user).values_list('amount', 'description', 'category', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response



def export_pdf(request):
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename=Expenses'+ str(datetime.datetime.now()) +'.pdf'
    # response['Content-Transfer-Encoding'] = 'binary'
    # context = {
    #     'expenses': [],
    #     'total': 0,
    # }
    # html_string = render_to_string('expenses/pdf_output.html', context)
    # html = HTML(string=html_string)
    # result = html.write_pdf()


    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()

    #     output = open(output.name, 'rb')
    #     response.write(output.read())

    # return response
    pass
