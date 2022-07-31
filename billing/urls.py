from django.urls import path
from . import views
from billingsoftware.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('', views.chart, name='chart'),
    path('viewinvoices/', views.index, name='index'),
    path('detail/<str:id>/', views.viewInvoice, name='viewInvoice'),
    path('create/', views.createInvoice, name='viewInvoice'),
    path('createinvoice/<str:uid>/', views.createInvoicefucntion,
         name='createinvoice'),
    path('save/<str:uid>/<int:total>/<int:costumer_id>/', views.SaveInvoice,
         name='SaveInvoice'),
    path('print/<str:uid>/', views.printInvoice),
    path('payments/history/<str:uid>/', views.paymentsHistory),
    path('delete/<str:uid>/', views.deleteInvoice),
    path('delete/item/<int:id>/<str:uid>/', views.deleteItem),
    path('delete/item/onbill/<int:id>/<str:uid>/', views.deleteItemonBill),
    path('create/product/view/', views.createProduct),
    path('delete/product/view/<int:id>/', views.deleteProduct),
    path('reports/view/', views.reports),
    path('costumers/view/', views.Customers),
    path('costumers/delete/<int:id>/', views.costumersDelete),
    path('create/costumer/', views.createCostumer),
    path('payments/create/<str:id>/', views.paymentsCreate),
    path('create/new/payment/<str:id>/<str:balance>/<str:paid>/', views.NewPayment),
    path('success/<str:message>/', views.success),
    path('searchinvoice/', views.searchinvoice),
    path('costumerdetail/<str:uid>/', views.costumerdetail),
    path('expenses/', views.expenses),
    path('expenses/dashboard/', views.expensesdashboard),
    path('expenses/create/', views.createexpenses),
    path('chart/', views.chart),
    path('api/chart/', views.chartData),
#     path('test/', views.WorkTest),
]
