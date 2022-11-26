from django.contrib import admin
from . import models

admin.site.site_header = "Welcome to Professional Fuel Station Management System Portal"
admin.site.site_title = "PFSMS Admin Portal"
admin.site.index_title = "PFSMS Admin"

admin.site.register(models.System_Dependences)
admin.site.register(models.Account_Setting)
admin.site.register(models.Cash_Transaction)
admin.site.register(models.Summary)
admin.site.register(models.CCTV_Camera)
admin.site.register(models.Expense)
admin.site.register(models.Debtor_Detail)
admin.site.register(models.Debtor_Due)
admin.site.register(models.Employee_Detail)
admin.site.register(models.Employee_Salary)
admin.site.register(models.Supplier_Detail)
admin.site.register(models.Fuel_Supply)
admin.site.register(models.Fuel_Stock)
