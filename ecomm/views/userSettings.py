from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from ..models import Customer, ProductType, Product, ProductOrder, PaymentType, Order

@login_required
def userSettings(request):
    # sql = '''
    #     SELECT * FROM ecomm_user WHERE id=%s
    #     '''
    # user = User.objects.raw(sql, [pk])[0]
    currentUserId = request.user.id
    customer = Customer.objects.raw('''SELECT * FROM ecomm_customer where user_id=%s''',[currentUserId])[0]
    payments = PaymentType.objects.raw('''
        SELECT * from ecomm_paymentType
        JOIN ecomm_customer
        ON ecomm_customer.user_id  = ecomm_paymentType.customer_id
        JOIN auth_user
        ON  auth_user.id = ecomm_customer.user_id
        WHERE auth_user.id =%s
    ''', [currentUserId])
    history = ProductOrder.objects.raw('''
        SELECT * from ecomm_productorder
        JOIN ecomm_order
        ON ecomm_productorder.order_id  = ecomm_order.id
        JOIN ecomm_customer
        ON ecomm_customer.id = ecomm_order.buyer_id
        JOIN auth_user
        ON  auth_user.id = ecomm_customer.user_id
        JOIN ecomm_product
        ON ecomm_product.id = ecomm_productorder.product_id
        WHERE auth_user.id =%s
    ''', [currentUserId])
    context = {'customer' : customer, 'payments' : payments, 'history' : history}
    return render(request, 'ecomm/userSettings.html', context)
    # order = ProductOrder.objects.raw('SELECT * from ecomm_order')
