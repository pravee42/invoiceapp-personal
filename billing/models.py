from django.db import models
import datetime

# Create your models here.
class Invoice(models.Model):
    costumer_name = models.CharField(max_length=100)
    costumer_id = models.IntegerField(default=0)
    customer_gst_number = models.CharField(max_length=100, blank=True)
    billnumber = models.CharField(max_length=100)
    totalammount = models.IntegerField(default=0)
    invoice_type = models.CharField(max_length=100, default="Cash")
    discount = models.CharField(max_length=100, default=0)
    ammountpaid = models.IntegerField(default=0)
    due_date = models.CharField(max_length=100, default=datetime.date.today())
    collectedby = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

    @property
    def is_due(self):
        return datetime.date.today() > datetime.datetime.strptime(
            self.due_date, "%Y-%m-%d").date()
        
    @property
    def is_total(self):
        diff = self.totalammount - self.ammountpaid
        if diff > 20:
            return False
        else:
            True
    @property
    def balance(self):
        return self.totalammount - self.ammountpaid

    def __str__(self):
        return self.billnumber


class InvoiceBills(models.Model):
    invoice = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    qty = models.IntegerField(default=1)
    price = models.FloatField(default=0.1)
    gst = models.FloatField(default=0.1)
    totalammount = models.IntegerField(default=0)


class Products(models.Model):
    product_name = models.CharField(max_length=100)
    purchase_ammount = models.FloatField(default=0)
    product_price = models.FloatField(default=0)
    gst = models.FloatField(default=0)


class Costumersmodel(models.Model):
    costumer_name = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    pincode = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    credit_ammount = models.IntegerField(default=0)
    paid_ammount = models.IntegerField(default=0)


class Payments(models.Model):
    invoice = models.CharField(max_length=100)
    costumer_name = models.CharField(max_length=100)
    refrence_number = models.CharField(max_length=100)
    ammount = models.CharField(max_length=100, default=0)
    pan = models.CharField(max_length=100, blank=True)
    date_created = models.CharField(max_length=100, default=str(datetime.date.today()))


class Test(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

class Expenses(models.Model):
    expense_name = models.CharField(max_length=100)
    ammount = models.DecimalField(max_digits=10, decimal_places=2)
    costumer_name = models.CharField(max_length=100, default='Non Billable Expense')
    notes = models.TextField(blank=True)
    date = models.CharField(max_length=100, default=str(datetime.date.today()))

class DraftInvoices(models.Model):
    invoice_number = models.CharField(max_length=100)
    
class Services(models.Model):
    taskid= models.CharField(max_length=100, blank=True)
    service_number = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    ammount = models.IntegerField(default=0)
    paid = models.IntegerField(default=0)
    costumer_name = models.CharField(max_length=100, default="General Service")
    contact_number = models.CharField(max_length=100)

class ServicePayments(models.Model):
    service_number = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    ammount = models.IntegerField(default=0)
    refrence_number = models.CharField(max_length=100, default="01234")
    paymentmode= models.CharField(max_length=100, default='cash')
    
class Calendar(models.Model):
    date = models.CharField(max_length=100)
    task = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    contact_number = models.CharField(max_length=100, default="00000000000")
    costumer_name = models.CharField(max_length=100, default="GTS")
    completed = models.CharField(max_length=100, default="false")
    tasktype=models.CharField(max_length=100, default="task")

class ServiceWorks(models.Model):
    service_number = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    ammount = models.IntegerField(default=0)
