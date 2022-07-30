from django import forms
from .models import Invoice, InvoiceBills

class CreateInvoice(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
