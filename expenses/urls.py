from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expense/', views.add_expense, name="add-expense"),
    path('edit-expense/<int:id>/', views.edit_expense, name="edit-expense"),
    path('delete-expense/<id>/', views.delete_expense, name="delete-expense"),
    path('search-expenses/', csrf_exempt(views.search_expenses), name="search-expenses"),
    path('expense-category-summary/', views.expense_category_summary, name="expense-category-summary"),
    path('stats/', views.stats_view, name="stats"),
    path('export-csv/', views.export_csv, name="export-csv"),
    path('export-excel/', views.export_excel, name="export-excel"),
    path('export-pdf/', views.export_pdf, name="export-pdf"),
]
