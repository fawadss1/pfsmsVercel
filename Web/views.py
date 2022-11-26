from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from dateutil import relativedelta
from django.db.models import Q
from . import models
import datetime as T
import subprocess
import hashlib
import os

x = T.datetime.now()
y = T.datetime.now() - T.timedelta(days=1)
previous_date = y.strftime('%Y-%m-%d')
today_date = x.strftime('%Y-%m-%d')


def signup(request):
    if not models.System_Dependences.objects.exists():
        if request.method == 'POST':
            # Pump Account Information
            firstOwner = request.POST.get('first_owner').title()
            secondOwner = request.POST.get('second_owner').title()
            pumpName = request.POST.get('pump_name').title()
            firstMobNo = request.POST.get('first_mob_no')
            secondMobNo = request.POST.get('second_mob_no')
            email = request.POST.get('email')
            pumpAddress = request.POST.get('pump_add').title()
            totalBalance = request.POST.get('total_balance')
            username = request.POST.get('username')
            password = request.POST.get('confirm_password')
            # prices & stocks
            petrolPrice = request.POST.get('petrol_price')
            dieselPrice = request.POST.get('diesel_price')
            # Machines Readings
            petrolReadingA = request.POST.get('petrol_readingA')
            petrolReadingB = request.POST.get('petrol_readingB')
            petrolReadingC = request.POST.get('petrol_readingC')
            petrolReadingD = request.POST.get('petrol_readingD')
            dieselReadingA = request.POST.get('diesel_readingA')
            dieselReadingB = request.POST.get('diesel_readingB')
            summaryDate = request.POST.get('summary_date')
            # Get Fuel Supplier Details
            petrolStock = request.POST.get('petrol_stock')
            petrolRs = request.POST.get('petrolRs')
            dieselStock = request.POST.get('diesel_stock')
            dieselRs = request.POST.get('dieselRs')
            supplierName = request.POST.get('supplier_name').title()
            supplierMobNo = request.POST.get('mob_no')
            residentAddress = request.POST.get('res_address').title()
            companyName = request.POST.get('company_name').title()
            iban = request.POST.get('iban').title()
            bankName = request.POST.get('bank_name').title()

            if User.objects.filter(username=username):
                messages.error(request, 'Sorry This Username Already Taken Try Another One')
                return redirect('/Login')
            else:
                hwName = os.getenv('COMPUTERNAME')
                hwId = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
                # password = ' %546 ' + hashlib.sha256(password.encode('utf-8')).hexdigest() + ' 546% '
                admin = User.objects.create_superuser(username, email, password)
                admin.save()
                models.System_Dependences(Admin=admin, Hardware_Name=hwName, Hardware_Id=hwId).save()
                obj = models.Supplier_Detail(Admin=admin, Name=supplierName, Mobile=supplierMobNo,
                                             Resident_Address=residentAddress, Company_Name=companyName, IBAN=iban,
                                             Bank_Name=bankName)
                obj.save()
                models.Fuel_Supply(Supply_Date=summaryDate, Supplier_ID=obj, Petrol_Supplied_Ltrs=petrolStock,
                                   Petrol_Supply_Rs=petrolRs, Diesel_Supplied_Ltrs=dieselStock,
                                   Diesel_Supply_Rs=dieselRs).save()
                models.Account_Setting(Admin=admin, First_Owner=firstOwner, Second_Owner=secondOwner, Owner_Email=email,
                                       First_Owner_Mobile=firstMobNo, Secon_Owner_Mobile=secondMobNo,
                                       Pump_Name=pumpName,
                                       Pump_Address=pumpAddress, Pump_Reg_No='PSO-01').save()
                obj = models.Summary(Admin=admin, Date=summaryDate, Petrol_Price=petrolPrice, Diesel_Price=dieselPrice,
                                     Petrol_ReadingA=petrolReadingA, Petrol_ReadingB=petrolReadingB,
                                     Petrol_ReadingC=petrolReadingC, Petrol_ReadingD=petrolReadingD,
                                     Total_Petrol_Sold=0,
                                     Total_Petrol_Rs=0, Diesel_ReadingA=dieselReadingA, Diesel_ReadingB=dieselReadingB,
                                     Total_Diesel_Sold=0, Total_Diesel_Rs=0, Today_Sale_Man='-', Tonight_Sale_Man='-',
                                     Today_Total_Expenses=0, Today_Total_Credit=0, Today_Total_Debit=0, Today_Rs=0)
                obj.save()
                models.Fuel_Stock(Admin=admin, Date=obj, Total_Petrol_In_Stock=petrolStock,
                                  Total_Diesel_In_Stock=dieselStock).save()
                cashOut = float(petrolRs) + float(dieselRs)
                models.Cash_Transaction(Admin=admin, Date=obj, Cashed_In=0, Cashed_In_Reason='-', Cashed_Out=cashOut,
                                        Cashed_Out_Reason=f'Fuel Cash Paid To {supplierName}',
                                        Total_Month_Rs=totalBalance).save()
                data = {'firstOwner': firstOwner, 'pumpName': pumpName, 'pumpAddress': pumpAddress,
                        'username': username,
                        'password': password}
                content = render_to_string('Mails/Welcome_Message.html', {'data': data})
                sendEmail(request, "Welcome Message", content)
                messages.success(request, 'Your Account Has Been Created Please Login')
                return redirect('/Login')
    else:
        return redirect('Login')
    return render(request, 'SignUp.html')


def loginUser(request):
    if models.System_Dependences.objects.exists():
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # password = ' %546 ' + hashlib.sha256(password.encode('utf-8')).hexdigest() + ' 546% '
            if models.Account_Setting.objects.count() < 1 or User.objects.count() < 1:
                messages.error(request, 'Sorry You Donot Have An Account SignUp First')
                return redirect('/Login')
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    data = [models.Account_Setting.objects.last()]
                    content = render_to_string('Mails/Login_Alert.html', {'data': data, 'user': request.user})
                    sendEmail(request, "login Alert", content)
                    if models.Login_Statistics.objects.filter(Admin=request.user, Time=x.strftime('%I:%M:%S %p')):
                        models.Login_Statistics.objects.filter(Admin=request.user,
                                                               Time=x.strftime('%I:%M:%S %p')).delete()
                    models.Login_Statistics(Admin=request.user, Time=x.strftime('%I:%M:%S %p'), Date=today_date).save()
                    request.session['login'] = True
                    request.session.modified = True
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('/')
                else:
                    messages.error(request, 'Invalid Login Credentials Try Again')
                    return render(request, 'Login.html')
    else:
        return redirect('Signup')
    return render(request, 'Login.html')


def recoverPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username) or User.objects.filter(email=username):
            messages.success(request, f' Well Be Updated Soon')
        else:
            messages.error(request, f'Invalid Username Or Email')
    return render(request, 'Recover_Password.html')


def logoutUser(request):
    logout(request)
    return redirect('/Login')


def notifications(request):
    global empSalaries
    if request.user.is_anonymous:
        return {'empSalaries': None}
    else:
        stock = [models.Fuel_Stock.objects.last()]
        for i in stock:
            if i.Total_Petrol_In_Stock <= 1500 or i.Total_Diesel_In_Stock <= 1500:
                return {'lowFuel': True}
        if models.Employee_Detail.objects.count() < 1 or not models.Employee_Detail.objects.filter(Admin=request.user):
            empSalaries = None
        employee = models.Employee_Detail.objects.filter(Admin=request.user)
        for emp in employee:
            if not models.Employee_Salary.objects.filter(Employee_ID=emp, Salary_Date__month=x.strftime('%m'),
                                                         Salary_Status='Fully Paid'):
                empSalaries = models.Employee_Detail.objects.filter(Name=emp, Admin=request.user)
                return {'empSalaries': empSalaries}
            else:
                empSalaries = None
        return {'empSalaries': empSalaries}


def admin(request):
    return {'Admin': request.user}


@login_required(login_url='/Login')
def settings(request):
    if not models.Summary.objects.filter(Admin=request.user):
        messages.error(request, 'Sorry! You Dont Have Any Record Please SignUp First Thank You')
    else:
        if request.method == 'POST' and 'changeSetting' in request.POST:
            recordId = request.POST.get('id')
            petrolPrice = request.POST.get('petrol_price')
            dieselPrice = request.POST.get('diesel_price')
            models.Summary.objects.filter(id=recordId).update(Petrol_Price=petrolPrice, Diesel_Price=dieselPrice)
            messages.success(request, 'Account Setting Has Been Updated')

        if request.method == 'POST' and 'changePass' in request.POST:
            oldPass = request.POST.get('oldpass')
            newPass = request.POST.get('newPass')
            oldPassword = '%546 ' + hashlib.sha256(oldPass.encode('utf-8')).hexdigest() + '546%'
            newPassword = '%546 ' + hashlib.sha256(newPass.encode('utf-8')).hexdigest() + '546%'
            user = authenticate(username=request.user, password=oldPassword)
            if user is not None:
                u = User.objects.get(username=request.user)
                u.set_password(newPassword)
                u.save()
                messages.success(request, 'Account Password Has Been Changed\nPlease Login Agian')
                return redirect('#')
            else:
                messages.error(request, 'Sorry! Invalid Password Try Again')
        fuelData = [models.Summary.objects.filter(Admin=request.user).last()]
        cashData = [models.Cash_Transaction.objects.filter(Admin=request.user).last()]
        return render(request, 'Settings.html',
                      {'fuelData': fuelData, 'cashData': cashData})
    return render(request, 'Settings.html')


@login_required(login_url='/Login')
def profile(request):
    if not models.Summary.objects.filter(Admin=request.user):
        messages.error(request, 'Sorry! You Dont Have Any Record Please SignUp First Thank You')
    else:
        if request.method == 'POST':
            firstOwner = request.POST.get('first_owner').title()
            secondOwner = request.POST.get('second_owner').title()
            pumpName = request.POST.get('pump_name').title()
            firstMobNo = request.POST.get('first_mob_no')
            secondMobNo = request.POST.get('second_mob_no')
            email = request.POST.get('email')
            regNo = request.POST.get('reg_no')
            pumpAddress = request.POST.get('address').title()
            models.Account_Setting.objects.filter(Admin=request.user).update(First_Owner=firstOwner,
                                                                             Second_Owner=secondOwner,
                                                                             Owner_Email=email,
                                                                             First_Owner_Mobile=firstMobNo,
                                                                             Secon_Owner_Mobile=secondMobNo,
                                                                             Pump_Name=pumpName,
                                                                             Pump_Address=pumpAddress,
                                                                             Pump_Reg_No=regNo)
            messages.success(request, 'Profile Has Been Updated')
        if not models.Account_Setting.objects.filter(Admin=request.user):
            messages.error(request, 'Sorry! You Dont Have Any Record Please Signup First')
        else:
            AccountData = models.Account_Setting.objects.filter(Admin=request.user)
            Transictions = models.Cash_Transaction.objects.filter(Admin=request.user)
            loginStatistics = models.Login_Statistics.objects.filter(Admin=request.user).order_by('-id')
            return render(request, 'Profile.html',
                          {'data': AccountData, 'Transictions': Transictions, 'loginStatistics': loginStatistics})
    return render(request, 'Profile.html')


@login_required(login_url='/Login')
def dashboard(request):
    global context
    totalPetrolSoldM = 0
    totalDieselSoldM = 0
    totalPetrolRs = 0
    totalDieselRs = 0
    if not models.Summary.objects.filter(Admin=request.user):
        messages.error(request, 'Sorry! You Dont Have Any Record Please SignUp First Thank You')
    else:
        boxes = [models.Summary.objects.filter(Admin=request.user).last()]
        employee = models.Employee_Detail.objects.filter(Admin=request.user)
        fuelStock = [models.Fuel_Stock.objects.filter(Admin=request.user).last()]
        if not models.Summary.objects.filter(Admin=request.user, id__gte=2, Date__month=x.strftime('%m')):
            currentMonthData = models.Summary.objects.filter(Admin=request.user, id__gte=2)[:20]
        else:
            currentMonthData = models.Summary.objects.filter(Admin=request.user, id__gte=2,
                                                             Date__month=x.strftime('%m'))
        for i in currentMonthData:
            totalPetrolSoldM += float(i.Total_Petrol_Sold)
            totalDieselSoldM += float(i.Total_Diesel_Sold)
            totalPetrolRs += float(i.Total_Petrol_Rs)
            totalDieselRs += float(i.Total_Diesel_Rs)
            # month_list = models.Summary.objects.dates('Date', 'month')
            # for j in month_list:
            #     currentYearData = models.Summary.objects.filter(Admin=request.user, Date__month=j.month,
            #                                                     Date__year=x.strftime('%Y'))
            #     totalPetrolSoldY = 0
            #     totalDieselSoldY = 0
            #     for k in currentYearData:
            #         totalPetrolSoldY += float(k.Total_Petrol_Sold)
            #         totalDieselSoldY += float(k.Total_Diesel_Sold)
            # context = {'boxes': boxes, 'employee': employee, 'currentMonth': currentMonthData,
            #            'currentYear': currentYearData, 'PetrolSoldM': totalPetrolSoldM, 'DieselSoldM': totalDieselSoldM,
            #            'PetrolSoldY': totalPetrolSoldY, 'DieselSoldY': totalDieselSoldY, 'fuelStock': fuelStock}
        context = {'boxes': boxes, 'employee': employee, 'currentMonth': currentMonthData,
                   'PetrolSoldM': totalPetrolSoldM, 'DieselSoldM': totalDieselSoldM, 'PetrolRsM': totalPetrolRs,
                   'DieselRsM': totalDieselRs, 'fuelStock': fuelStock}
        return render(request, 'Dashboard.html', context)
    return render(request, 'Dashboard.html')


@login_required(login_url='/Login')
def addSummary(request):
    global total_balance, newDieselStock, newPetrolStock, previous_petrol_stock, previous_diesel_stock, totalMonthRs, debtors
    today_total_expenses = 0
    today_total_credit = 0
    today_total_debt = 0
    if request.method == 'POST' and 'FuelChecked' in request.POST:
        petrol_checked = request.POST.get('petrol_checked')
        diesel_checked = request.POST.get('diesel_checked')
        previousFuel = [models.Fuel_Stock.objects.filter(Admin=request.user).last()]
        obj = models.Summary.objects.latest('Date')
        for f in previousFuel:
            newPetrolStock = f.Total_Petrol_In_Stock + float(petrol_checked)
            newDieselStock = f.Total_Diesel_In_Stock + float(diesel_checked)
            if models.Fuel_Stock.objects.filter(Admin=request.user, Date=obj):
                models.Fuel_Stock.objects.filter(Admin=request.user, Date=obj).delete()
                models.Fuel_Stock(Admin=request.user, Date=obj, Total_Petrol_In_Stock=newPetrolStock,
                                  Total_Diesel_In_Stock=newDieselStock).save()
            else:
                models.Fuel_Stock(Admin=request.user, Date=obj, Total_Petrol_In_Stock=newPetrolStock,
                                  Total_Diesel_In_Stock=newDieselStock).save()
        messages.info(request, 'Fuel Has Been Added Back To Stock')

    if request.method == 'POST' and 'addFuel' in request.POST:
        new_petrol_stock = request.POST.get('petrol_stock')
        new_diesel_stock = request.POST.get('diesel_stock')
        supplierId = request.POST.get('supplier')
        supplyDate = request.POST.get('supply_date')
        petrol_rs = request.POST.get('petrol_rs')
        diesel_rs = request.POST.get('diesel_rs')
        cashOut = float(petrol_rs) + float(diesel_rs)
        previousCash = [models.Cash_Transaction.objects.filter(Admin=request.user).last()]
        for cash in previousCash:
            total_balance = cash.Total_Month_Rs - float(cashOut)
        previousFuel = [models.Fuel_Stock.objects.filter(Admin=request.user).last()]
        obj = models.Summary.objects.latest('Date')
        for f in previousFuel:
            newPetrolStock = f.Total_Petrol_In_Stock + float(new_petrol_stock)
            newDieselStock = f.Total_Diesel_In_Stock + float(new_diesel_stock)
        for supplier in models.Supplier_Detail.objects.filter(id=supplierId):
            if models.Cash_Transaction.objects.filter(Admin=request.user, Date__Date=supplyDate):
                models.Cash_Transaction.objects.filter(Admin=request.user, Date__Date=supplyDate).delete()
            models.Cash_Transaction(id=obj.id, Admin=request.user, Date=obj, Cashed_In=0, Cashed_In_Reason='-',
                                    Cashed_Out=cashOut, Cashed_Out_Reason=f'Fuel Cash Paid To {supplier.Name}',
                                    Total_Month_Rs=total_balance).save()
            if models.Fuel_Supply.objects.filter(Supplier_ID=supplier, Supply_Date=supplyDate):
                models.Fuel_Supply.objects.filter(Supply_Date=supplyDate, Supplier_ID=supplier).delete()
            models.Fuel_Supply(Supply_Date=supplyDate, Supplier_ID=supplier, Petrol_Supplied_Ltrs=new_petrol_stock,
                               Petrol_Supply_Rs=petrol_rs, Diesel_Supplied_Ltrs=new_diesel_stock,
                               Diesel_Supply_Rs=diesel_rs).save()
            if models.Fuel_Stock.objects.filter(Admin=request.user, Date=obj):
                models.Fuel_Stock.objects.filter(Admin=request.user, Date=obj).delete()
            models.Fuel_Stock(id=obj.id, Admin=request.user, Date=obj, Total_Petrol_In_Stock=newPetrolStock,
                              Total_Diesel_In_Stock=newDieselStock).save()
            messages.success(request, 'Fuel New Stock Has Been Added')

    if request.method == 'POST' and 'addSummary' in request.POST:
        summaryDate = request.POST.get('summary_date')
        if models.Fuel_Stock.objects.filter(Date__Date=summaryDate):
            previousFuel = [models.Fuel_Stock.objects.filter(Admin=request.user).order_by('-id')[1]]
        else:
            previousFuel = [models.Fuel_Stock.objects.filter(Admin=request.user).last()]
        # Fetching previous Data from DB
        for f in previousFuel:
            # Previous Fuel inStock
            previous_petrol_stock = f.Total_Petrol_In_Stock
            previous_diesel_stock = f.Total_Diesel_In_Stock

        # Total Month Balance
        if models.Cash_Transaction.objects.filter(Admin=request.user, Date__Date=summaryDate):
            balance = [models.Cash_Transaction.objects.filter(Admin=request.user).order_by('-id')[1]]
        else:
            balance = [models.Cash_Transaction.objects.filter(Admin=request.user).last()]
        for B in balance:
            totalMonthRs = B.Total_Month_Rs

        # Machines Readings
        if models.Summary.objects.filter(Admin=request.user, Date=summaryDate):
            machineData = [models.Summary.objects.filter(Admin=request.user).order_by('-id')[1]]
        else:
            machineData = [models.Summary.objects.filter(Admin=request.user).last()]
        for i in machineData:
            previous_petrol_readingA = i.Petrol_ReadingA
            previous_petrol_readingB = i.Petrol_ReadingB
            previous_petrol_readingC = i.Petrol_ReadingC
            previous_petrol_readingD = i.Petrol_ReadingD
            previous_diesel_readingA = i.Diesel_ReadingA
            previous_diesel_readingB = i.Diesel_ReadingB

            # previous Summary ID
            summaryID = i.id + 1

            # Taking New Data From User
            new_petrol_price = request.POST.get('petrol_price')
            new_diesel_price = request.POST.get('diesel_price')

            # Machines Readings
            new_petrol_readingA = request.POST.get('petrol_reading_A')
            new_petrol_readingB = request.POST.get('petrol_reading_B')
            new_petrol_readingC = request.POST.get('petrol_reading_C')
            new_petrol_readingD = request.POST.get('petrol_reading_D')
            new_diesel_readingA = request.POST.get('diesel_reading_A')
            new_diesel_readingB = request.POST.get('diesel_reading_B')

            # Sale Man Name and Date
            DaySaleMan = request.POST.get('day_sale_man')
            NightSaleMan = request.POST.get('night_sale_man')

            # Rupees
            today_expenses = request.POST.getlist('today_expenses')
            today_expenses_list = request.POST.getlist('expenses_list')

            while True:
                try:
                    today_expenses.remove('')
                    today_expenses_list.remove('')
                except ValueError:
                    break
            for exp in today_expenses:
                if exp == '':
                    today_total_expenses = 0
                else:
                    today_total_expenses += float(exp)
            # Debtors
            today_cash_debit = request.POST.getlist('total_cash_debit')
            today_cash_credit = request.POST.getlist('total_cash_credit')

            # Litters Sold Today
            petrol_sold_A = float(new_petrol_readingA) - float(previous_petrol_readingA)
            petrol_sold_B = float(new_petrol_readingB) - float(previous_petrol_readingB)
            petrol_sold_C = float(new_petrol_readingC) - float(previous_petrol_readingC)
            petrol_sold_D = float(new_petrol_readingD) - float(previous_petrol_readingD)
            diesel_sold_A = float(new_diesel_readingA) - float(previous_diesel_readingA)
            diesel_sold_B = float(new_diesel_readingB) - float(previous_diesel_readingB)

            # Total Sold in Litters
            total_petrol_sold = petrol_sold_A + petrol_sold_B + petrol_sold_C + petrol_sold_D
            total_diesel_sold = diesel_sold_A + diesel_sold_B

            # Stock of Petrol And Diesel
            remain_petrol_stock = float(previous_petrol_stock) - total_petrol_sold
            remain_diesel_stock = float(previous_diesel_stock) - total_diesel_sold

            # Rupees of Petrol and Diesel
            petrol_rupees = float(total_petrol_sold) * float(new_petrol_price)
            diesel_rupees = float(total_diesel_sold) * float(new_diesel_price)

            # Creating Debtors Record Data
            if not models.Debtor_Due.objects.filter(Debt_Date=summaryDate):
                totalDayRs = float(petrol_rupees) + float(diesel_rupees)
            else:
                models.Debtor_Due.objects.filter(Debt_Date=summaryDate).delete()
            debtorID = models.Debtor_Detail.objects.filter(Admin=request.user)
            previousDebtorDues = models.Debtor_Due.objects.filter(~Q(Debt_Date=summaryDate))
            for j in range(
                    len(today_cash_debit) and len(today_cash_credit) and len(debtorID) or len(previousDebtorDues)):
                if today_cash_credit[j] == '' or today_cash_debit[j] == '':
                    today_cash_debit[j] = 0
                    today_cash_credit[j] = 0
                today_total_credit += float(today_cash_credit[j])
                today_total_debt += float(today_cash_debit[j])
                totalDebt = float(previousDebtorDues.values_list('Current_Total_Debt', flat=True)[j]) + float(
                    today_cash_debit[j]) - float(today_cash_credit[j])
                models.Debtor_Due(Debt_Date=summaryDate, Debtor_ID=debtorID[j], Today_Debt=today_cash_debit[j],
                                  Today_Credit=today_cash_credit[j], Current_Total_Debt=totalDebt).save()
            # Expenses Plus Debit
            todayCashOut = float(today_total_debt) + float(today_total_expenses)

            # Total Day Rupees
            totalDayRs = float(petrol_rupees) + float(diesel_rupees) + float(today_total_credit) - float(todayCashOut)

            # Total Month Rupees
            updatedTotalMonthRs = float(totalMonthRs) + totalDayRs

            # Creating Summary Data Object in DB
            if models.Summary.objects.filter(Admin=request.user, Date=summaryDate):
                models.Summary.objects.filter(Admin=request.user, Date=summaryDate).delete()
                messages.warning(request, 'Record Has Been Updated')
            else:
                messages.success(request, 'Record Has Been Added')
            obj = models.Summary(Admin=request.user, id=summaryID, Date=summaryDate,
                                 Petrol_Price=new_petrol_price, Diesel_Price=new_diesel_price,
                                 Petrol_ReadingA=new_petrol_readingA, Petrol_ReadingB=new_petrol_readingB,
                                 Petrol_ReadingC=new_petrol_readingC, Petrol_ReadingD=new_petrol_readingD,
                                 Total_Petrol_Sold=total_petrol_sold, Total_Petrol_Rs=petrol_rupees,
                                 Diesel_ReadingA=new_diesel_readingA, Diesel_ReadingB=new_diesel_readingB,
                                 Total_Diesel_Sold=total_diesel_sold, Total_Diesel_Rs=diesel_rupees,
                                 Today_Sale_Man=DaySaleMan, Tonight_Sale_Man=NightSaleMan,
                                 Today_Total_Expenses=today_total_expenses, Today_Total_Credit=today_total_credit,
                                 Today_Total_Debit=today_total_debt, Today_Rs=totalDayRs)
            obj.save()
            for j in range(len(today_expenses) and len(today_expenses_list)):
                models.Expense(Admin=request.user, Date=obj, Expense_Name=today_expenses_list[j].title(),
                               Expense_Price=today_expenses[j]).save()
            models.Cash_Transaction(Admin=request.user, Date=obj, Cashed_In=0, Cashed_In_Reason='-', Cashed_Out=0,
                                    Cashed_Out_Reason='-', Total_Month_Rs=updatedTotalMonthRs).save()
            # Creating Fuel Data Object in DB
            if models.Fuel_Stock.objects.filter(Date__Date=summaryDate):
                models.Fuel_Stock.objects.filter(Date__Date=summaryDate).delete()
            models.Fuel_Stock(Admin=request.user, Date=obj, Total_Petrol_In_Stock=remain_petrol_stock,
                              Total_Diesel_In_Stock=remain_diesel_stock).save()

    if not models.Summary.objects.filter(Admin=request.user):
        messages.error(request, 'Sorry! You Do not Have An Account Please SignUp')
    else:
        d = models.Summary.objects.latest('Date')
        if models.Summary.objects.filter(Admin=request.user, id__gt=1, Date=d.Date):
            previous_machine_data = [models.Summary.objects.filter(Admin=request.user).order_by('-id')[1]]
        else:
            previous_machine_data = [models.Summary.objects.filter(Admin=request.user).last()]
        current_machine_data = [models.Summary.objects.filter(Admin=request.user).latest('Date')]
        count = models.Debtor_Detail.objects.count()
        debtors = models.Debtor_Due.objects.filter(Debtor_ID__Admin_id=request.user).order_by('-id')[:count]
        saleMen = models.Employee_Detail.objects.filter(Admin=request.user, Role='Sale Man')
        suppliers = models.Supplier_Detail.objects.filter(Admin=request.user)
        fuel = [models.Fuel_Stock.objects.filter(Admin=request.user).last()]
        balance = [models.Cash_Transaction.objects.filter(Admin=request.user).last()]
        machineData = zip(current_machine_data, previous_machine_data)
        context4 = {'machine_data': machineData, 'debtor_data': debtors, 'date': x.strftime('%d'),
                    'todayDate': today_date, 'previousDate': previous_date, 'sale_men': saleMen,
                    'suppliers': suppliers, 'fuel': fuel, 'balance': balance, }
        return render(request, 'Add_Summary.html', context4)
    return render(request, 'Add_Summary.html')


@login_required(login_url='/Login')
def viewSummaries(request):
    global data
    if not models.Summary.objects.filter(Admin=request.user):
        messages.error(request, 'Sorry! You Do not Have An Account Please SignUp')
    elif request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        date = request.POST.get('date')
        if date:
            if not models.Summary.objects.filter(Admin=request.user, id__gt=1, Date=date):
                return JsonResponse({'error': f'Sorry! You Do Not Have Any Record At ({date})'})
            else:
                data = models.Summary.objects.filter(Admin=request.user, id__gt=1, Date=date).values()
                return JsonResponse({'data': list(data)})
        else:
            if not models.Summary.objects.filter(Admin=request.user, id__gt=1, Date__month=month, Date__year=year):
                return JsonResponse({'error': f'Sorry! You Do Not Have Any Record At ({month}/{year})'})
            else:
                data = models.Summary.objects.filter(Admin=request.user, id__gte=2, Date__month=month,
                                                     Date__year=year).order_by('-id').values()
                return JsonResponse({'data': list(data)})
    fDate = models.Summary.objects.values_list('Date', flat=True).first()
    lDate = models.Summary.objects.values_list('Date', flat=True).last()
    return render(request, 'View_Summaries.html', {'fDate': fDate, 'lDate': lDate})


@login_required(login_url='/Login')
def printSummary(request, summary_id, date):
    current_summary = models.Summary.objects.filter(Admin=request.user, id=summary_id)
    previous_summary = models.Summary.objects.filter(Admin=request.user, id=summary_id - 1)
    todayExpenses = models.Expense.objects.filter(Admin=request.user, Date__Date=date)
    pump_name = models.Account_Setting.objects.filter(Admin=request.user)
    previousDayRs = [models.Cash_Transaction.objects.filter(Admin=request.user, Date__Date__lt=date).order_by('-id')[0]]
    totalMonthRs = [models.Cash_Transaction.objects.filter(Admin=request.user, Date__Date=date).last()]
    debtors = models.Debtor_Due.objects.filter(Debt_Date=date)
    fuelStock = models.Fuel_Stock.objects.filter(Admin=request.user, Date__Date=date)
    if models.Fuel_Stock.objects.filter(Admin=request.user, Date__Date=date):
        PreviousFuel = [models.Fuel_Stock.objects.filter(Admin=request.user).order_by('-id')[1]]
    else:
        PreviousFuel = [models.Fuel_Stock.objects.filter(Admin=request.user).last()]
    context5 = {'previous_data': previous_summary, 'current_data': current_summary, 'expenses': todayExpenses,
                'pump_name': pump_name, 'debtors': debtors, 'currentFuelStock': fuelStock,
                'previousFuelStock': PreviousFuel, 'totalMonthRs': totalMonthRs, 'previousDayRs': previousDayRs}
    return render(request, 'Print_Summary.html', context5)


@login_required(login_url='/Login')
def addDebtor(request):
    if request.method == 'POST':
        debtor_name = request.POST.get('debtor_name').title()
        father_name = request.POST.get('father_name').title()
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        cnic = request.POST.get('cnic')
        resident_address = request.POST.get('res_address').title()
        current_debt = request.POST.get('current_debt')
        supply_date = request.POST.get('supply_date')
        if not models.Debtor_Detail.objects.filter(Name=debtor_name):
            obj_debtor = models.Debtor_Detail(Admin=request.user, Name=debtor_name, Father_Name=father_name,
                                              Email=email, Mobile=mob_no, CNIC=cnic, Resident_Address=resident_address)
            obj_debtor.save()
            models.Debtor_Due(Debt_Date=supply_date, Debtor_ID=obj_debtor, Today_Credit=0,
                              Today_Debt=current_debt, Current_Total_Debt=current_debt).save()
            messages.success(request, f'{debtor_name} Record Has Been Added')
        else:
            messages.warning(request, f'Debtor {debtor_name} Record Already Exits')
    smryDate = models.Summary.objects.latest('Date')
    return render(request, 'Add_Debtor.html', {'Date': smryDate})


@login_required(login_url='/Login')
def viewDebtors(request):
    if not models.Debtor_Detail.objects.filter(Admin=request.user):
        messages.error(request, 'Sorry! You Dont Have Any Debtor Registered')
    else:
        debtorInfo = models.Debtor_Detail.objects.filter(Admin=request.user).order_by('-id')
        debtorDue = models.Debtor_Due.objects.order_by('-id')
        view_debtor = zip(debtorInfo, debtorDue)
        return render(request, 'View_Debtors.html', {'debtors': view_debtor})
    return render(request, 'View_Debtors.html')


@login_required(login_url='/Login')
def editDebtor(request, debtorId):
    global debtorDues, debtorsCount, debtorsEntryDate
    if request.method == 'POST' and 'Updated' in request.POST:
        debtor_name = request.POST.get('debtor_name').title()
        father_name = request.POST.get('father_name').title()
        mob_no = request.POST.get('mob_no')
        cnic = request.POST.get('cnic')
        resident_address = request.POST.get('res_address').title()
        models.Debtor_Detail.objects.filter(Admin=request.user, id=debtorId).update(Name=debtor_name,
                                                                                    Father_Name=father_name, CNIC=cnic,
                                                                                    Mobile=mob_no,
                                                                                    Resident_Address=resident_address)
        messages.success(request, f'{debtor_name} Record Has Been Updated')
        return redirect('/Debtors/View-Debtors')
    if request.method == 'POST' and 'Deleted' in request.POST:
        models.Debtor_Detail.objects.filter(Admin=request.user, id=debtorId).delete()
        messages.error(request, 'Debtor Record Has Been Deleted')
        return redirect('/Debtors/View-Debtors')
    debtorDetails = models.Debtor_Detail.objects.filter(Admin=request.user, id=debtorId)
    saleMan = models.Summary.objects.filter(Admin=request.user, id__gte=2)
    debtorDuesDetail = models.Debtor_Due.objects.filter(Debtor_ID=debtorId)
    debtorDuesDetails = zip(debtorDuesDetail, saleMan)
    for i in debtorDetails:
        debtorDues = models.Debtor_Due.objects.filter(Debtor_ID=i.id).order_by('-id')
        debtorsCount = models.Debtor_Due.objects.filter(Debtor_ID=i.id).count()
        debtorsEntryDate = models.Debtor_Due.objects.filter(Debtor_ID=i.id).first()
    debtor = zip(debtorDetails, debtorDues)
    context3 = {'DebtorDetails': debtor, 'debtorCount': debtorsCount, 'debtorEntryDate': debtorsEntryDate,
                'debtorDuesDetails': debtorDuesDetails}
    return render(request, 'Edit_Debtor.html', context3)


@login_required(login_url='/Login')
def addEmployee(request):
    if request.method == 'POST':
        employee_name = request.POST.get('employee_name').title()
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        cnic = request.POST.get('cnic')
        role = request.POST.get('role')
        salary = request.POST.get('salary')
        doj = request.POST.get('doj')
        resident_address = request.POST.get('res_address').title()
        if not models.Employee_Detail.objects.filter(Name=employee_name, Mobile=mob_no):
            models.Employee_Detail(Admin=request.user, Date_of_Join=doj, Name=employee_name, Email=email, Mobile=mob_no,
                                   Resident_Address=resident_address, CNIC=cnic, Role=role, Salary=salary).save()
            messages.success(request, f'{employee_name} Record Has Been Added')
        else:
            messages.warning(request, f'{employee_name} Record Already Exits')
    return render(request, 'Add_Employee.html')


@login_required(login_url='/Login')
def viewEmployees(request):
    if not models.Employee_Detail.objects.filter(Admin=request.user):
        messages.error(request, 'Sorry! You Dont Have Any Employee Registered')
    else:
        employeeInfo = models.Employee_Detail.objects.filter(Admin=request.user)
        return render(request, 'View_Employees.html', {'employee': employeeInfo})
    return render(request, 'View_Employees.html')


@login_required(login_url='/Login')
def editEmployee(request, employeeId):
    global debtorDues, debtorsCount, TotalMonthRs, serviceTime
    if request.method == 'POST' and 'salarypaid' in request.POST:
        PreviousMonthRs = [models.Cash_Transaction.objects.last()]
        for i in PreviousMonthRs:
            TotalMonthRs = i.Total_Month_Rs
        emp_name = request.POST.get('emp_name')
        basic_Salary = request.POST.get('basic_salary')
        total_salary_paid = request.POST.get('salary_paid')
        salary_status = request.POST.get('salary_status')
        remain_salary = int(basic_Salary) - int(total_salary_paid)
        updatedTotalMonthRs = float(TotalMonthRs) - float(total_salary_paid)
        for j in models.Employee_Detail.objects.filter(id=employeeId):
            if models.Employee_Salary.objects.filter(Employee_ID=j, Salary_Date__month=x.strftime('%m')):
                models.Employee_Salary.objects.filter(Employee_ID=j, Salary_Date__month=x.strftime('%m')).delete()
            models.Employee_Salary(Salary_Date=today_date, Employee_ID=j, Total_Paid_Rs=total_salary_paid,
                                   Total_Remained_Rs=remain_salary, Salary_Status=salary_status).save()
        obj = models.Summary.objects.last()
        if models.Cash_Transaction.objects.filter(Admin=request.user, Date__Date=today_date):
            models.Cash_Transaction.objects.filter(Admin=request.user, Date__Date=today_date).delete()
        models.Cash_Transaction(Admin=request.user, Date=obj, Cashed_In=0, Cashed_In_Reason='-',
                                Cashed_Out=total_salary_paid, Cashed_Out_Reason=f'Salary Piad To {emp_name}',
                                Total_Month_Rs=updatedTotalMonthRs).save()
        messages.success(request, f'Salary Paid To {emp_name}')

    if request.method == 'POST' and 'Update' in request.POST:
        employee_name = request.POST.get('name').title()
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        cnic = request.POST.get('cnic')
        resident_address = request.POST.get('res_address').title()
        role = request.POST.get('role')
        salary = request.POST.get('salary')
        models.Employee_Detail.objects.filter(id=employeeId).update(Name=employee_name, Email=email, Mobile=mob_no,
                                                                    CNIC=cnic, Resident_Address=resident_address,
                                                                    Role=role, Salary=salary)
        models.Employee_Salary.objects.filter(id=employeeId).update(Salary_Date=today_date, Salary_Status='Not Paid')
        messages.success(request, f'{employee_name} Record Has Been Updated')
        return redirect('/Employees/View-Employees')
    if request.method == 'POST' and 'Delete' in request.POST:
        models.Employee_Detail.objects.filter(id=employeeId).delete()
        messages.error(request, 'Employee Record Has Been Deleted')
        return redirect('/Employees/View-Employees')

    employeeInfo = models.Employee_Detail.objects.filter(id=employeeId)
    pumpInfo = models.Account_Setting.objects.filter(Admin=request.user)
    employeeSalaryDetails = models.Employee_Salary.objects.filter(Employee_ID=employeeId)
    if not models.Employee_Salary.objects.filter(Employee_ID=employeeId, Salary_Date__month=x.strftime('%m'),
                                                 Salary_Status='Fully Paid'):
        employeeSalary = models.Employee_Detail.objects.filter(Admin=request.user)
    else:
        employeeSalary = None

    for i in employeeInfo:
        dateNow = x.strptime(today_date, '%Y-%m-%d')
        delta = relativedelta.relativedelta(dateNow, i.Date_of_Join)
        serviceTime = f"{delta.years} Years {delta.months} Months  {delta.days} Days"
    context2 = {'pumpInfo': pumpInfo, 'EmployeeDetails': employeeInfo, 'salaryDetails': employeeSalaryDetails,
                'salary': employeeSalary, 'serviceTime': serviceTime}
    return render(request, 'Edit_Employee.html', context2)


@login_required(login_url='/Login')
def addSupplier(request):
    if request.method == 'POST':
        supplier_name = request.POST.get('supplier_name').title()
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        iban = request.POST.get('iban').title()
        bank_name = request.POST.get('bank_name').title()
        resident_address = request.POST.get('res_address').title()
        company_name = request.POST.get('company_name').title()
        if not models.Supplier_Detail.objects.filter(Name=supplier_name):
            models.Supplier_Detail(Admin=request.user, Name=supplier_name, Email=email, Mobile=mob_no, IBAN=iban,
                                   Bank_Name=bank_name, Resident_Address=resident_address,
                                   Company_Name=company_name).save()
            messages.success(request, f'{supplier_name} Record Has Been Added ')
        else:
            messages.warning(request, f'{supplier_name} Record Already Exits')
    return render(request, 'Add_Supplier.html')


@login_required(login_url='/Login')
def viewSuppliers(request):
    if not models.Supplier_Detail.objects.filter(Admin=request.user):
        messages.error(request, 'Sorry! You Dont Have Any Supplier Registered')
    else:
        suppliers = models.Supplier_Detail.objects.filter(Admin=request.user)
        return render(request, 'View_Supplier.html', {'suppliers': suppliers})
    return render(request, 'View_Supplier.html')


@login_required(login_url='/Login')
def editSupplier(request, supplierId):
    totalPetrolSupplied = 0
    totalPetrolSuppliedRs = 0
    totalDieselSupplied = 0
    totalDieselSuppliedRs = 0
    if request.method == 'POST' and 'Updated' in request.POST:
        supplier_name = request.POST.get('supplier_name').title()
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        iban = request.POST.get('iban')
        bank_name = request.POST.get('bank_name').title()
        resident_address = request.POST.get('res_address').title()
        company_name = request.POST.get('company_name').title()
        models.Supplier_Detail.objects.filter(id=supplierId).update(Name=supplier_name, Email=email, Mobile=mob_no,
                                                                    IBAN=iban, Bank_Name=bank_name,
                                                                    Resident_Address=resident_address,
                                                                    Company_Name=company_name)
        messages.success(request, f'{supplier_name} Record Has Been Updated ')
        return redirect('/Suppliers/View-Supplier')
    if request.method == 'POST' and 'Deleted' in request.POST:
        models.Supplier_Detail.objects.filter(id=supplierId).delete()
        messages.error(request, 'Supplier Record Has Been Deleted')
        return redirect('/Suppliers/View-Supplier')
    supplier = models.Supplier_Detail.objects.filter(Admin=request.user, id=supplierId)
    fuel_Supplies = models.Fuel_Supply.objects.filter(Supplier_ID=supplierId)
    for i in fuel_Supplies:
        totalPetrolSupplied += i.Petrol_Supplied_Ltrs
        totalPetrolSuppliedRs += i.Petrol_Supply_Rs
        totalDieselSupplied += i.Diesel_Supplied_Ltrs
        totalDieselSuppliedRs += i.Diesel_Supply_Rs
    context3 = {'supplier': supplier, 'fuelSupplies': fuel_Supplies, 'petrolSupplied': totalPetrolSupplied,
                'dieselSupplied': totalDieselSupplied, 'petrolSuppliedRs': totalPetrolSuppliedRs,
                'dieselSuppliedRs': totalDieselSuppliedRs}
    return render(request, 'Edit_Supplier.html', context3)


@login_required(login_url='/Login')
def moneyCounter(request):
    return render(request, 'Money_Counter.html')


@login_required(login_url='/Login')
def posReciept(request):
    debtors = models.Debtor_Detail.objects.filter(Admin=request.user)
    pumpInfo = models.Account_Setting.objects.filter(Admin=request.user)
    fuelPrices = [models.Summary.objects.filter(Admin=request.user).last()]
    return render(request, 'Point_of_Sale.html', {'debtors': debtors, 'pumpInfo': pumpInfo, 'fuelPrices': fuelPrices})


@login_required(login_url='/Login')
def SecurityCameras(request):
    if request.method == 'POST':
        ipAddress = request.POST.get('ipAddress')
    dvrData = [models.CCTV_Camera.objects.last()]
    return render(request, 'Security_Cameras.html', {'dvrData': dvrData})


def notFound(request, exception):
    return render(request, '404.html')


@login_required(login_url='/Login')
def sendEmail(request, subject, content):
    email = models.Account_Setting.objects.values_list('Owner_Email', flat=True).last()
    try:
        send_mail(subject, "", "From PFSMS", [email], html_message=content, fail_silently=False)
        print(f'Email has Be Sent To {email} In Subject of {subject}')
    except Exception as e:
        print(f'{subject} Email Cannot Be Sent Due To {e}')
