from django.urls import path
from . import views

handler404 = 'Web.views.notFound'
urlpatterns = [
    path('Signup', views.signup, name="Signup"),
    path('Login', views.loginUser, name="Login"),
    path('Recover-Password', views.recoverPassword, name="Recover Password"),
    path('Accout-Settings', views.settings, name="Settings"),
    path('Accout-Profile', views.profile, name="Profile"),
    path('', views.dashboard, name="Dashboard"),
    path('Summaries/Add-Summary', views.addSummary, name="Add Summary"),
    path('Summaries/View-Summaries', views.viewSummaries, name="View Summaries"),
    path('Summaries/View-Summaries/Print-Summ/D<date>&-SNo<int:summary_id>', views.printSummary, name="Print Summary"),
    path('Debtors/Add-Debtor', views.addDebtor, name="Add Debtor"),
    path('Debtors/View-Debtors', views.viewDebtors, name="View Debtors"),
    path('Debtors/View-Debtors/Edit-No#<debtorId>', views.editDebtor, name="Edit Debtor"),
    path('Employees/Add-Employee', views.addEmployee, name="Add Employee"),
    path('Employees/View-Employees', views.viewEmployees, name="View Employees"),
    path('Employees/View-Employees/Edit-No#<employeeId>', views.editEmployee, name="Edit Employee"),
    path('Suppliers/Add-Supplier', views.addSupplier, name="Add Supplier"),
    path('Suppliers/View-Supplier', views.viewSuppliers, name="View Supplier"),
    path('Suppliers/View-Suppliers/Edit-No#<supplierId>', views.editSupplier, name="Edit Supplier"),
    path('Money-Counter-Calculator', views.moneyCounter, name="Money Counter"),
    path('Security-Cameras', views.SecurityCameras, name="Security Cameras"),
    path('Point-Of-Sale', views.posReciept, name="Point Of Sale"),
    path('Logout', views.logoutUser, name="Logout"),
]
