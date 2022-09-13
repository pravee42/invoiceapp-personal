from django.shortcuts import render, redirect
from .models import Invoice, InvoiceBills, Products, Payments, Costumersmodel, Test, Expenses, DraftInvoices, Calendar, Services, ServiceWorks, ServicePayments
from django.http import HttpResponse, JsonResponse
import secrets
from django.db.models import Case, Value, When, Count, Sum

from .forms import CreateInvoice
from random import randint
from num2words import num2words
import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def index(request):
    invoices = Invoice.objects.all()
    totalpaid = Invoice.objects.all().values("ammountpaid")
    totalammount = Invoice.objects.all().values("totalammount")
    toady_date = str(datetime.date.today())
    paid = 0
    for m in totalpaid:
        paid += int(m["ammountpaid"])
    total = 0
    for x in totalammount:
        total += int(x["totalammount"])
    overall = total - paid
    return render(
        request,
        "index.html",
        {"data": invoices, "paid": paid, "totalammount": total, "overall": overall},
    )


def viewInvoice(request, id):
    try:
        invoice = InvoiceBills.objects.filter(invoice=id)
        invoices = Invoice.objects.get(billnumber=id)
        balance = 0
        total_paid = Payments.objects.filter(invoice=id).values("ammount")
        sum_paid = 0
        for m in total_paid:
            sum_paid += int(m["ammount"])
        balance = int(invoices.totalammount) - int(sum_paid)
        return render(
            request,
            "invoicedetail.html",
            {"data": invoice, "indata": invoices, "balance": int(balance)},
        )
    except Invoice.DoesNotExist:
        return render(request, "errorpages/norecord.html", {'title': 'Invoice Not found'} ,status=status.HTTP_404_NOT_FOUND)


def createInvoice(request):
    if request.method == "POST":
        uid = request.POST["uid"]
        item = request.POST["item"]
        price = request.POST["price"]
        qty = request.POST["qty"]
        gst = request.POST["gst"]
        totalammount = request.POST["totalammount"]
        InvoiceBills.objects.create(
            invoice=uid,
            item=item,
            price=price,
            qty=qty,
            gst=gst,
            totalammount=totalammount,
        )
        filters = InvoiceBills.objects.filter(invoice=uid)
        products = Products.objects.all()
        return render(
            request,
            "newInvoice.html",
            {
                "today_date": str(datetime.date.today()),
                "uid": uid,
                "products": products,
                "datas": filters,
            },
        )
    products = Products.objects.all()
    return render(
        request,
        "newInvoice.html",
        {
            "today_date": str(datetime.date.today()),
            "uid": random_with_N_digits(5),
            "products": products,
        },
    )


def createInvoicefucntion(request, uid):
    invoices = InvoiceBills.objects.filter(invoice=uid)
    ammounts = InvoiceBills.objects.filter(invoice=uid).values("totalammount")
    x = 0
    for m in ammounts:
        x += int(m["totalammount"])
    costumers = Costumersmodel.objects.all()
    return render(
        request,
        "invoicefinal.html",
        {
            "today_date": str(datetime.date.today()),
            "uid": uid,
            "total": x,
            "datas": invoices,
            "costumers": costumers,
        },
    )


def SaveInvoice(request, uid, total, costumer_id):
    costumer_name = request.POST["costumer_name"]
    customer_gst_number = request.POST["customer_gst_number"]
    discount = request.POST["discount"]
    totalammount = request.POST["totalammount"]
    refrence_number = request.POST["refrence_number"]
    invoice_type = request.POST["invoice_type"]
    paid = request.POST["paid"]
    due_date = request.POST["due_date"]
    Invoice.objects.create(
        costumer_name=costumer_name,
        costumer_id=costumer_id,
        customer_gst_number=customer_gst_number,
        billnumber=uid,
        totalammount=totalammount,
        invoice_type=invoice_type,
        discount=discount,
        ammountpaid=paid,
        due_date=due_date,
        collectedby="user",
        date=str(datetime.date.today()),
    )
    Payments.objects.create(
        invoice=uid,
        costumer_name=costumer_name,
        refrence_number=refrence_number,
        ammount=paid,
    )
    if costumer_id != 0:
        cs_data = Costumersmodel.objects.get(id=costumer_id)
        cs_data.credit_ammount = int(cs_data.credit_ammount) + int(totalammount)
        if invoice_type == "Cash":
            cs_data.paid_ammount = int(cs_data.paid_ammount) + int(paid)
        if int(paid) > 0:
            cs_data.paid_ammount = int(cs_data.paid_ammount) + int(paid)
        cs_data.save()
    invoice = InvoiceBills.objects.filter(invoice=uid)
    invoices = Invoice.objects.get(billnumber=uid)
    url = '/detail/' + uid
    return redirect(url)

def printInvoice(request, uid):
    invoice = InvoiceBills.objects.filter(invoice=uid)
    invoices = Invoice.objects.get(billnumber=uid)
    invoicegst = InvoiceBills.objects.filter(invoice=uid).values("gst")
    gst_total = 0
    balance = int(invoices.totalammount) - int(invoices.ammountpaid)
    ammount_words = num2words(int(invoices.totalammount))
    ammount_words = " ".join(
        word[0].upper() + word[1:] for word in ammount_words.split(" ")
    )
    for m in invoicegst:
        gst_total += int(m["gst"])
    return render(
        request,
        "print.html",
        {
            "uid": uid,
            "data": invoice,
            "indata": invoices,
            "gst": gst_total,
            "balance": balance,
            "ammount_words": ammount_words,
        },
    )


def deleteInvoice(request, uid):
    try:
        delete = Invoice.objects.get(billnumber=uid)
        del_payemnts = Payments.objects.filter(invoice=uid)
        for m in del_payemnts:
            m.delete()
    except Invoice.DoesNotExist:
        return redirect("index")
    delete.delete()
    return redirect("index")


def deleteItem(request, id, uid):
    try:
        delete = InvoiceBills.objects.get(id=id)
    except InvoiceBills.DoesNotExist:
        return redirect("viewInvoice")
    delete.delete()
    return viewInvoice(request, uid)


def createBill1(request, uid):
    filters = InvoiceBills.objects.filter(invoice=uid)
    return render(
        request,
        "newInvoice.html",
        {"today_date": str(datetime.date.today()), "uid": uid, "datas": filters},
    )


def deleteItemonBill(request, id, uid):
    try:
        delete = InvoiceBills.objects.get(id=id)
    except InvoiceBills.DoesNotExist:
        return redirect("viewInvoice")
    delete.delete()
    return createBill1(request, uid)


def createProduct(request):
    data = Products.objects.all()
    if request.method == "POST":
        product_name = request.POST["product_name"]
        product_price = request.POST["product_price"]
        gst = request.POST["gst"]
        Products.objects.create(
            product_name=product_name, product_price=product_price, gst=gst
        )
        data = Products.objects.all()
        return render(request, "newProduct.html", {"products": data})
    else:
        return render(request, "newProduct.html", {"products": data})


def deleteProduct(request, id):
    try:
        delete = Products.objects.get(id=id)
    except Products.DoesNotExist:
        return redirect("/create/product/view/")
    delete.delete()
    return redirect("/create/product/view/")


def reports(request):
    if request.method == "POST":
        start = request.POST["from_date"]
        end = request.POST["to_date"]
        data = Invoice.objects.filter(date__range=[start, end])
        data1 = Invoice.objects.filter(date__range=[start, end]).values("ammountpaid")
        totalammount = Invoice.objects.filter(date__range=[start, end]).values(
            "totalammount"
        )
        sum = 0
        for m in data1:
            sum += int(m["ammountpaid"])
        total = 0
        for x in totalammount:
            total += int(x["totalammount"])
        overall = total - sum
        return render(
            request,
            "reports.html",
            {
                "data": data,
                "total": sum,
                "start": start,
                "end": end,
                "totalammount": total,
                "overall": overall,
            },
        )
    else:
        return render(request, "reports.html")


def paymentsHistory(request, uid):
    data = Payments.objects.filter(invoice=uid)
    total_paid = Payments.objects.filter(invoice=uid).values("ammount")
    sum_paid = 0
    for m in total_paid:
        sum_paid += int(m["ammount"])
    data1 = Invoice.objects.get(billnumber=uid)
    balance = int(data1.totalammount) - int(sum_paid)
    total = int(sum_paid) + int(balance)
    purchase1 = data1.totalammount + int(
        ((data1.totalammount) * int(data1.discount)) / 100
    )
    purchase = data1.totalammount + int(((purchase1) * int(data1.discount)) / 100)
    return render(
        request,
        "payments.html",
        {
            "data": data,
            "totalPaid": sum_paid,
            "balance": balance,
            "total": total,
            "data1": data1,
            "purchase": purchase,
        },
    )


def Customers(request):
    data = Costumersmodel.objects.all()
    return render(request, "costumers.html", {"data1": data})


def costumersDelete(request, id):
    try:
        delete = Costumersmodel.objects.get(id=id)
    except Costumersmodel.DoesNotExist:
        return redirect("/costumers/view/")
    delete.delete()
    return redirect("/costumers/view/")


def createCostumer(request):

    if request.method == "POST":
        costumer_name = request.POST["costumer_name"]
        gst_number = request.POST["gst_number"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        contact = request.POST["contact"]
        Costumersmodel.objects.create(
            costumer_name=costumer_name,
            gst_number=gst_number,
            address=address,
            pincode=pincode,
            contact=contact,
        )
        url = "/success/" + "Customer Created Successfully You may close this Tab"
        return redirect(url)
    return render(request, "createCostumer.html")


def paymentsCreate(request, id):
    invoice = InvoiceBills.objects.filter(invoice=id)
    payments = Payments.objects.filter(invoice=id)
    invoices = Invoice.objects.get(billnumber=id)
    balance = 0
    total_paid = Payments.objects.filter(invoice=id).values("ammount")
    sum_paid = 0
    for m in total_paid:
        sum_paid += int(m["ammount"])
    balance = int(invoices.totalammount) - int(sum_paid)

    return render(
        request,
        "newPayment.html",
        {
            "balance": balance,
            "invoice": invoices,
            "payment": payments,
            "paid": sum_paid,
        },
    )


def NewPayment(request, id, balance, paid):
    if request.method == "POST":
        costumer_name = request.POST["costumer_name"]
        refrence_number = request.POST["refrence_number"]
        ammount = request.POST["ammount"]
        update_data = Invoice.objects.get(billnumber=id)
        newAmmount = int(paid) + int(ammount)
        update_data.ammountpaid = newAmmount
        update_data.save()
        Payments.objects.create(
            invoice=id,
            costumer_name=costumer_name,
            refrence_number=refrence_number,
            ammount=ammount,
        )
        try:
            cs_data = Costumersmodel.objects.get(id=update_data.costumer_id)
            cs_data.paid_ammount = int(cs_data.paid_ammount) + int(ammount)
            cs_data.save()
        except Costumersmodel.DoesNotExist:
            pass
    url = "/success/" + "Payment Updated Successfully You may close this Tab"
    return redirect(url)


def success(request, message):
    return render(request, "success.html", {"message": message})


def searchinvoice(request):
    id = request.POST["invoiceid"]
    url = "/detail/" + id
    return redirect(url)

def costumerdetail(request, uid):
    invoices = Invoice.objects.filter(costumer_id=uid)
    costumer = Costumersmodel.objects.get(id=uid)
    return render(request, "costumerdetail.html", {"data1": invoices, 'costumer': costumer})


# def WorkTest(request):
#     x = Test.objects.annotate(or_price=Case(When(discount_price__isnull=True, then='price'), When(
#         discount_price__isnull=False, then='discount_price'))).values_list('or_price')
#     print(x)
#     return render(request, "base.html")


def expenses(request):
    if request.method == "POST":
        expense_name = request.POST['expense_name']
        date = request.POST['date']
        costumer_name = request.POST['costumer_name']
        ammount = request.POST['ammount']
        notes = request.POST['notes']
        Expenses.objects.create(expense_name=expense_name, ammount=ammount, costumer_name=costumer_name, notes=notes, date=date)
        return redirect('/expenses/dashboard/')
    return render(request, "expenses/expenses.html")


def expensesdashboard(request):
    expense = Expenses.objects.all()
    return render(request, "expenses/expensesdashboard.html", {"exp": expense})


def createexpenses(request):
    return render(request, "expenses/createexpense.html")

@api_view(['GET'])
def chartData(request):
    expense = Expenses.objects.all().values('ammount')
    sale = Invoice.objects.all().values('totalammount')
    sale_dates = (Invoice.objects
                  .values('date')
                  .annotate(ammount=Sum('totalammount')).order_by('date'))
    return Response(sale_dates)

def chart(request):
    expense = Expenses.objects.all().values('ammount')
    sale = Invoice.objects.all().values('totalammount')
    sum_paid = 0
    for m in expense:
        sum_paid += int(m["ammount"])
    sum_sale = 0
    for m in sale:
        sum_sale += int(m["totalammount"])
    payments = Payments.objects.all().values('ammount')
    sum_payments = 0
    for m in payments:
        sum_payments += int(m["ammount"])
    invoices = Invoice.objects.all().order_by('-id')[:5]
    return render(request, 'dashboard.html', {'expense': sum_paid, 'sale': sum_sale, 'payments': sum_payments, 'invoices': invoices})


@api_view(['GET'])
def apiChartExpense(request):
    sale_dates = (Expenses.objects
                  .values('date')
                  .annotate(ammount=Sum('ammount')).order_by('date'))
    return Response(sale_dates)

def search_products(request, stra):
    products = Products.objects.filter(product_name__icontains=stra).values(
        'product_name', 'product_price', 'gst')
    return JsonResponse(list(products), safe=False)

def EditExpenses(request, expId):
    expenses = Expenses.objects.get(id=expId)
    if request.method == "POST":
        expense_name = request.POST['expense_name']
        date = request.POST['date']
        costumer_name = request.POST['costumer_name']
        ammount = request.POST['ammount']
        notes = request.POST['notes']
        expenses.expense_name=expense_name
        expenses.ammount=ammount
        expenses.costumer_name=costumer_name
        expenses.notes=notes
        expenses.date=date
        expenses.save()
        return redirect('/expenses/dashboard/')
    else:
        return render(request, 'expenses/editExpense.html', {'expense': expenses})

def DeleteExpense(request, pk):
    try:
        delete = Expenses.objects.get(id=pk)
    except Expenses.DoesNotExist:
        return render(request, 'errorpages/norecord.html', {'title': 'Expense Not Found'})
    delete.delete()
    return redirect("/expenses/dashboard/")

def editInvoice(request, pk):
    if request.method == "POST":
        pass
    del_payemnts = Payments.objects.filter(invoice=pk)
    for m in del_payemnts:
        m.delete()
    inv = Invoice.objects.get(billnumber=pk)
    inv.delete()
    DraftInvoices.objects.create(invoice_number=pk)
    url = '/createinvoice/'+pk
    return redirect(url)
    
def DraftInvoice(request):
    getdrafts = DraftInvoices.objects.all()
    return render(request, 'draftInvoice.html', {'invoice': getdrafts})


def DeleteDraftInvoice(request, pk):
    dd = DraftInvoices.objects.get(invoice_number=pk)
    dd.delete()
    url = '/'
    return redirect(url)


def CalendarView(request, pk):
    if pk == "task":
        data = Calendar.objects.filter(tasktype=pk)
        return render(request, "calendar/task.html", {'data': data, 'tt': pk})
    else:
        data = Calendar.objects.filter(tasktype=pk)
        return render(request, "calendar/task.html", {'data': data, 'tt': pk})


def CalendarDetail(request, pk):
    data = Calendar.objects.get(id=pk)
    return render(request, "calendar/taskdetail.html", {'data': data})

def CalendarAcceptDeleteTask(request, pk, url1, method): 
    if method == 'accept':
        data = Calendar.objects.get(id=pk)
        data.completed = "accepted"
        data.save()
        url = '/calendar/view/' + url1
        return redirect(url)
    elif method == 'delete':
       data = Calendar.objects.get(id=pk)
       data.delete()
       url = '/calendar/view/' + url1
       return redirect(url)
    elif method == 'complete':
        data = Calendar.objects.get(id=pk)
        data.completed = "true"
        data.save()
        url = '/calendar/view/' + url1
        return redirect(url)

def CalendarCreateTask(request):
    if request.method == "POST":
        date = request.POST['date']
        task = request.POST['task']
        notes = request.POST['notes']
        contact_number = request.POST['contact_number']
        costumer_name = request.POST['costumer_name']
        completed = 'false'
        tasktype = request.POST['tasktype']
        url = '/calendar/view/' + tasktype
        Calendar.objects.create(date=date, task=task,notes=notes, contact_number=contact_number, costumer_name=costumer_name, completed=completed, tasktype=tasktype)
        return redirect(url)
    else:
        a = 'newa'
        return render(request, "calendar/newevent.html", {'tt': a})

def serviceProcess(request, pk):
    if request.method == "GET":
        calendar_data = Calendar.objects.get(id=pk)
        service_number = random_with_N_digits(11)
        try:
            services = Services.objects.get(taskid=pk)
            try:
                works = ServiceWorks.objects.filter(service_number=services.service_number).values('ammount')
                totalammount = 0
                for x in works:
                    totalammount += int(x['ammount'])
                services.ammount = totalammount
                services.save()
            except ServiceWorks.DoesNotExist:
                services = Services.objects.get(taskid=pk)
        except Services.DoesNotExist:
            taskid = pk
            date = str(datetime.date.today())
            ammount = 0
            paid = 0
            costumer_name = calendar_data.costumer_name
            contact_number = calendar_data.contact_number
            Services.objects.create(taskid=taskid, service_number=service_number, date=date,
                                    ammount=ammount, paid=paid, costumer_name=costumer_name, contact_number=contact_number)
        data = Services.objects.get(taskid=pk)     
        serviceworks = ServiceWorks.objects.filter(service_number=data.service_number)     
          
        return render(request, 'calendar/serviceprocess.html', {'service_number': service_number, 'servicedata': data, 'service': serviceworks})
    elif request.method == 'POST':
        services = Services.objects.get(taskid=pk)
        service = request.POST['service']
        ammount = request.POST['ammount']
        ServiceWorks.objects.create(service_number=services.service_number, service=service, ammount=ammount)
        url = '/calendar/event/service/process/'+pk+'/'
        return redirect(url)
    
def ErrorView(request, pk):
    return render(request, 'errorpages/error500.html', {'title':pk})

def completePaymentService(request, pk):
    if request.method == 'GET':
        service = Services.objects.get(service_number=pk)
        serviceitems = ServiceWorks.objects.filter(service_number=pk)
        return render(request, 'calendar/completeservice.html', {'service': service, 'products': serviceitems})
    else:
        ammount = request.POST['ammount']
        refrence_number = request.POST['refrence_number']
        mode = request.POST['mode']
        try:
            sss = Services.objects.get(service_number=pk)
            sss.paid = int(ammount)
            sss.save()
            ServicePayments.objects.create(
                service_number=pk, date=str(datetime.date.today()), ammount=ammount, refrence_number=refrence_number, paymentmode=mode)
            calendar = Calendar.objects.get(id=sss.taskid)
            calendar.completed = 'true'
            calendar.save()
            url = "/success/" + "Service Payment Updated Successfully You can close this tab"
            return redirect(url)
        except Services.DoesNotExist:
            url = "/error/" + "Error Updating Payment Service"
            return redirect(url)


def custom_error_404(request, exception):
    return render(request, 'errorpages/error500.html', {'title': 'Page Not found'})
