from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .filters import OrderFilter
from .models import *
from .forms import OrderForm,CreateUserForm, CustomerForm
from .decorators import unauthenticated_user,allowed_users ,admin_only


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username') # dic타입으로 입력한 4자료가 모두 날아옴
           
            messages.success(request, username+'님의 회원가입이 완료되었습니다')
            return redirect('login')
    
    context={
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.info(request, "아이디/비밀번호를 확인해주세요")
            
    context={}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()
    
    total_customers = customers.count()
    
    total_orders= orders.count()
    delivered = orders.filter(status='배송완료').count()
    pending = orders.filter(status='보류중').count()
    
    context={
        'orders':orders,
        'customers':customers,
        
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
    }
    return render(request, 'accounts/dashboard.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    a = Group.objects.get(name='customer')
  
    orders = request.user.customer.order_set.all()
    
    total_orders= orders.count()
    delivered = orders.filter(status='배송완료').count()
    pending = orders.filter(status='보류중').count()
    
    context={
        'orders':orders,
         'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
    }
    return render(request,'accounts/user.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method=="POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
            
    context={
        'form':form,
    }
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Products.objects.all()
    
    context={
        'products':products,
    }
    return render(request, 'accounts/products.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    
    orders=customer.order_set.all()
    total_count = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    print(orders," in views")
    context={
        'customer':customer,
         'orders':orders,
          'total_count':total_count,
        'myFilter':myFilter,
    }
    return render(request, 'accounts/customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),extra=5)
    customer = Customer.objects.get(id=pk)
    
    formset=OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method=="POST":
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={
      'formset':formset,
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method=="POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context={
        'form':form,
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def deleteOrder(request, pk):
    item = Order.objects.get(id=pk)
    
    if request.method=="POST":
        item.delete()
        return redirect('/')
    
    context={
        'item':item,
    }
    return render(request, 'accounts/delete.html', context)