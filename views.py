from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import timedelta

from .models import *
from .forms import CreateUserForm
from django.contrib.auth.models import User

# Create your views here.
#diseaseform function is to display Disease table form
def diseaseform(request):
    return render(request,'diseaseform.html')

#adddisease function is used to add diseases into database
def adddisease(request):
    if request.method == 'POST':
        name = request.POST.get('diseasename')
        data = Disease(name=name)
        data.save()
    return render(request,'diseaseform.html')

def hospital_form(request):
    diseases = Disease.objects.all()
    return render(request,'hospitalform.html',{'diseases':diseases})

def add_hospital_details(request):
    if request.method == "POST":
        name = request.POST.get('name')
        location = request.POST.get('location')
        data = Hospital(name=name,location = location)
        data.save()
        diseases = request.POST.getlist('diseases')
        for disease in diseases:
            data.diseases.add(disease)
        return HttpResponse('added')
    return render(request,'hospitalform.html')

def healthpolicy_form(request):
    diseases = Disease.objects.all()
    hospitals = Hospital.objects.all()
    return render(request,'healthpolicyform.html',{'diseases':diseases,'hospitals':hospitals})

def create_health_policy(request):
    if request.method == 'POST':
        policy_id = request.POST.get('policy_id')
        premium = request.POST.get('premium')
        tenure = request.POST.get('tenure')
        policy = Health_policy(policy_id=policy_id,premium=premium,tenure=tenure)
        policy.save()
        diseases = request.POST.getlist('diseases')
        # print(diseases)
        for disease in diseases:
            policy.covered_illnesses.add(disease)
        hospitals = request.POST.getlist('hospitals')
        # print(hospitals)
        for hospital in hospitals:
            policy.covered_hospitals.add(hospital)
        return HttpResponse('added')
    return render(request,'healthpolicyform.html')

def health_policy_customerform(request):
    users = User.objects.all()
    healthpolicies = Health_policy.objects.all()
    return render(request,'healthcustomerform.html',{'users':users,'healthpolicies':healthpolicies})

def add_health_policy_customerdetails(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            user = (User.objects.get(pk=name))
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            age = request.POST.get('age')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            # print([name,firstname,lastname,age,phone,address])
            customer = Customer(name=user,firstname=firstname,lastname=lastname,age=age,phone=phone,address=address)
            customer.save()
            policy_id = request.POST.get('healthpolicy')
            customer.health_policies.add(Health_policy.objects.get(pk = policy_id))
            customer.save()
            return HttpResponse('added')

def home(request):
    hospitals = Hospital.objects.all()
    policies = Health_policy.objects.all()
    # for i in policies:
    #     print(i.covered_hospitals.all())
    return render(request,'home.html',{'hospitals':hospitals,'policies': policies})

@login_required(login_url='login')
def health(request):
    policies = Health_policy.objects.all()
    return render(request,'policies.html',{'policies':policies})


# =======
def areaform(request):
    return render(request,'Areaform.html')

def add_arae_details(request):
    if request.method == 'POST':
        area = request.POST.get('name')
        amount = request.POST.get('amount')
        area_data = Area(name=area,amount=amount)
        area_data.save()
        return HttpResponse('/added/')
    return render(request,'Areaform.html')

def house_policy(request):
    areas =Area.objects.all()
    return render(request,'housepolicyform.html',{'areas':areas})

def premiumform(request):
    areas = Area.objects.all()
    return render(request,'premiumform.html',{'areas':areas})


# @login_required(login_url='login')
def count_premium(request):
    if request.method == "POST":
        name = request.POST.get('name')
        area = request.POST.get('area')
        amount =  Area.objects.get(id=area)
        monthly_amount = round((amount.amount/12),2)
        return render(request,'premiumcardpage.html',{'amount':amount,'monthly_amount':monthly_amount})

@login_required(login_url='login')
def housepaymentform(request):
    #messages.info(request, 'Username OR Password is Incorrect')
    areas = Area.objects.all()
    return render(request,'housepayment.html',{'areas':areas})

def house_payment_details(request):
    if request.method == "POST":
        user = request.user
        fullname = request.POST.get('fullname')
        
        location = request.POST.get('area')
        area = Area.objects.get(name=location)
        policy = House_policies(user=user,fullname=fullname,location=area)
        policy.save()
        area.count += 1
        policy_status = Pending_house_policies(policy=policy)
        policy_status.save()
        return redirect('home')

def pending_house_policies(request):
    policies = House_policies.objects.filter(status = 'Pending')
    print(policies)
    return render(request,'pendinghousepolicies.html',{'policies':policies})


def handle_house_polices(request):
    if request.method == "POST":
        if request.POST.get('accept'):
            user = request.user
            policy = House_policies.objects.get(pk=request.POST.get('accept'))
            pending_policies = policy.pending_house_policies
            print(user)
            policy.status = 'accepted'
            policy.save()
            approved_house_policies = Approved_house_policies(policy = policy)
            approved_house_policies.save()
            pending_policies.delete()
            messages.success(request, 'Policy accepted successfully')
            return redirect('pendingpolices')

            '''
            customer.status = 'accepted'
            customer.save()
            approved_policies = Approved_policies(policy = customer)
            approved_policies.save()
            pending_policies.delete()
            messages.success(request, 'Policy accepted successfully')
            return redirect('pendingpolices')'''

def approved_house_policies(request):
    policies = House_policies.objects.filter(status = 'accepted')
    print(policies)
    return render(request,'approved_house_policieslist.html',{'policies':policies})



# >>>>>>> bb12cb4693e647188469d9481c0fb8780e04f1cd

def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for👉🏽' + user)
            return redirect('login')
    context = {'form':form}
    return render(request, 'register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR Password is Incorrect')
        context = {}
        return render(request, 'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def getplan(request,id):
    policy = Health_policy.objects.get(id=id)
    total = policy.premium * 1.18
    # print (total)
    return render(request,'getnow.html',{'policy':policy,'total':total})

def orderpage(request):
    return render(request,'orderpage.html')

def policy_orderdetails(request, policy_id):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        age = request.POST.get('age')
        phone = request.POST.get('phonenumber')
        address = request.POST.get('address')
        print([firstname,lastname,age,phone,address])
        customer = Customer(name=request.user, firstname=firstname,lastname=lastname,age=age,phone=phone,address=address)
        customer.save()
        customer.health_policies.add(Health_policy.objects.get(pk = policy_id))
        customer.save()
        status = Pending_policies(policy=customer)
        status.save()
        return orderpage(request)


# @login_required(login_url='adminlogin')
def dashboard(request):
    return render(request,'admin_dashboard.html')

def healthpolicy_customers(request):
    customers = Customer.objects.all()
    duedate_lst = []
    for i in customers:
        purchasedate = i.purchase_date
        policies = i.health_policies.all()
        tenure = [i.tenure for i in policies][0]
        # print(tenure)
        duedate = purchasedate + (timedelta(days = (30 * tenure)))
        duedate_lst.append(duedate.strftime("%Y-%m-%d"))
        # print(duedate_lst)
        duedate_dict = {}
        for i in range(len(duedate_lst)):
            duedate_dict[str(i)] = duedate_lst[i]
        # print(duedate_dict)
        details = zip(customers,duedate_lst)
    return render(request,'healthpolicycustomers.html',{'details':details})

def diseaseslist(request):
    diseases = Disease.objects.all()
    return render(request,'diseaseslist.html',{'diseases':diseases})

def hospitalslist(request):
    hospitals = Hospital.objects.all()
    return render(request,'hospitalslist.html',{'hospitals':hospitals})

def healthpolicieslist(request):
    healthpolicies = Health_policy.objects.all()
    return render(request,'healthpolicieslist.html',{'healthpolicies':healthpolicies})

def no_of_signupUsers(request): 
    s1 = User.objects.all()
    context = {  
        's1':s1          
    }
    return render(request,'no_of_signupUser.html',context)
@login_required(login_url='login')
def customer_dashboard(request):     
    return render(request,'customer_dashboard.html')
    
def customer_apply(request):
    customer = request.user.customer_set.all()[0]
    policies = customer.health_policies.all()
    print(policies)
    return render(request,'customer_apply.html',{'policies':policies,'customer':customer})

def pending_policies(request):
    policies = Customer.objects.filter(status = 'Pending')
    print(policies)
    return render(request,'pendingpolicies.html',{'policies':policies})

def approved_health_policies(request):
    policies = Customer.objects.filter(status = 'accepted')
    print(policies)
    return render(request,'approved_health_policieslist.html',{'policies':policies})

def handle_polices(request):
    if request.method == "POST":
        if request.POST.get('accept'):
            customer = Customer.objects.get(pk = request.POST.get('accept'))
            pending_policies = customer.pending_policies
            print(customer)
            customer.status = 'accepted'
            customer.save()
            approved_policies = Approved_policies(policy = customer)
            approved_policies.save()
            pending_policies.delete()
            messages.success(request, 'Policy accepted successfully')
            return redirect('pendingpolices')