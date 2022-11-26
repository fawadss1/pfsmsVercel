from django.contrib.auth.models import User
from django.db import models


class System_Dependences(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Date_of_Installation = models.DateField(auto_now=True)
    Hardware_Name = models.CharField(max_length=100)
    Hardware_Id = models.CharField(max_length=255)

    def __str__(self):
        return 'Date Of Instalation ' + str(self.Date_of_Installation)

    class Meta:
        verbose_name_plural = "System Dependencies"


class Account_Setting(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    First_Owner = models.CharField(max_length=255)
    Second_Owner = models.CharField(max_length=255, default=None)
    Pump_Name = models.CharField(max_length=255)
    Pump_Address = models.CharField(max_length=255)
    First_Owner_Mobile = models.CharField(max_length=255)
    Secon_Owner_Mobile = models.CharField(max_length=255, default=None)
    Owner_Email = models.CharField(max_length=255)
    Pump_Reg_No = models.CharField(max_length=255)

    def __str__(self):
        return self.Pump_Name + " Account Section"

    class Meta:
        verbose_name_plural = "Account Details"


class Login_Statistics(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Time = models.CharField(max_length=25)
    Date = models.DateField()


class Summary(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.DateField(auto_now=False)
    Petrol_Price = models.FloatField()
    Diesel_Price = models.FloatField()
    Petrol_ReadingA = models.FloatField()
    Petrol_ReadingB = models.FloatField()
    Petrol_ReadingC = models.FloatField()
    Petrol_ReadingD = models.FloatField()
    Total_Petrol_Sold = models.FloatField()
    Total_Petrol_Rs = models.FloatField()
    # Diesel
    Diesel_ReadingA = models.FloatField()
    Diesel_ReadingB = models.FloatField()
    Total_Diesel_Sold = models.FloatField()
    Total_Diesel_Rs = models.FloatField()
    # Rs
    Today_Sale_Man = models.CharField(max_length=25)
    Tonight_Sale_Man = models.CharField(max_length=25)
    Today_Total_Expenses = models.FloatField()
    Today_Total_Credit = models.FloatField()
    Today_Total_Debit = models.FloatField()
    Today_Rs = models.FloatField()

    def __str__(self):
        return self.Date.strftime('%d/%b/%Y')

    class Meta:
        verbose_name_plural = "Summaries"


class Cash_Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.ForeignKey(Summary, on_delete=models.CASCADE)
    Cashed_In = models.FloatField()
    Cashed_In_Reason = models.CharField(max_length=255)
    Cashed_Out = models.FloatField()
    Cashed_Out_Reason = models.CharField(max_length=255)
    Total_Month_Rs = models.FloatField()

    def __str__(self):
        return str(self.Date)

    class Meta:
        verbose_name_plural = "Cash Transactions"


class Expense(models.Model):
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.ForeignKey(Summary, on_delete=models.CASCADE)
    Expense_Name = models.CharField(max_length=25)
    Expense_Price = models.IntegerField()

    def __str__(self):
        return str(self.Date)


class Debtor_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=25)
    Father_Name = models.CharField(max_length=25)
    Email = models.CharField(max_length=25)
    Mobile = models.CharField(max_length=15)
    CNIC = models.CharField(max_length=15)
    Resident_Address = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = "Debtor Details"


class Debtor_Due(models.Model):
    Debt_Date = models.DateField(auto_now=False)
    Debtor_ID = models.ForeignKey(Debtor_Detail, on_delete=models.CASCADE)
    Today_Credit = models.FloatField()
    Today_Debt = models.FloatField()
    Current_Total_Debt = models.FloatField()

    def __str__(self):
        return self.Debt_Date.strftime('%d/ %b/ %Y')
        # return "Debt Of " + str(self.Debtor_ID)

    class Meta:
        verbose_name_plural = "Debtor Dues"


class Employee_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Date_of_Join = models.DateField(auto_now=False)
    Name = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Mobile = models.CharField(max_length=25)
    CNIC = models.CharField(max_length=255)
    Resident_Address = models.CharField(max_length=255)
    Role = models.CharField(max_length=255)
    Salary = models.IntegerField()

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = "Employee Details"


class Employee_Salary(models.Model):
    Salary_Date = models.DateField(auto_now=False)
    Employee_ID = models.ForeignKey(Employee_Detail, on_delete=models.CASCADE)
    Total_Paid_Rs = models.IntegerField()
    Total_Remained_Rs = models.IntegerField()
    Salary_Status = models.CharField(max_length=20)

    def __str__(self):
        return str(self.Employee_ID)

    class Meta:
        verbose_name_plural = "Employees Salaries"


class Supplier_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=20)
    Email = models.CharField(max_length=20)
    Mobile = models.CharField(max_length=13)
    IBAN = models.CharField(max_length=20)
    Bank_Name = models.CharField(max_length=20)
    Company_Name = models.CharField(max_length=55)
    Resident_Address = models.CharField(max_length=30)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = "Supplier Details"


class Fuel_Supply(models.Model):
    Supply_Date = models.DateField(auto_now=False)
    Supplier_ID = models.ForeignKey(Supplier_Detail, on_delete=models.CASCADE)
    Petrol_Supplied_Ltrs = models.FloatField()
    Petrol_Supply_Rs = models.FloatField()
    Diesel_Supplied_Ltrs = models.FloatField()
    Diesel_Supply_Rs = models.FloatField()

    def __str__(self):
        return str(self.Supply_Date.strftime('%d/%b/%Y'))

    class Meta:
        verbose_name_plural = "Fuel Supplies"


class Fuel_Stock(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.ForeignKey(Summary, on_delete=models.CASCADE)
    Total_Petrol_In_Stock = models.FloatField()
    Total_Diesel_In_Stock = models.FloatField()

    def __str__(self):
        return str(self.Date)

    class Meta:
        verbose_name_plural = "Fuel Stock"


class CCTV_Camera(models.Model):
    id = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Ip_Address = models.CharField(max_length=15)
