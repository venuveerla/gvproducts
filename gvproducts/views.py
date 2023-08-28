from django.shortcuts import render,redirect
from django.db.models import Sum
from sms import send_sms
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages
import pandas as pd
from .models import *
import datetime
# Create your views here.
# details page redirection 
def home(request):
    return render(request,'home.html')
def registeration(request):
    return render(request,"details.html")
# register the details into database
def registered(request):
    output=''
    d={'name':"","gender":"",'father':"","village":"","mandal":"","district":"","phno1":"",'phno2':""}
    if(request.method=="POST"):
        name=request.POST.get('name')
        d['name']=name
        gender=request.POST.get('gender')
        d['gender']=gender
        father=request.POST.get('father')
        d['father']=father
        village=request.POST.get('village')
        d['village']=village
        mandal=request.POST.get('mandal')
        d['mandal']=mandal
        district=request.POST.get('district')
        d['district']=district
        phno1=request.POST.get('phno1')
        d['phno1']=phno1
        phno2=request.POST.get('phno2')
        d['phno2']=phno2
        balance=0
        var=insertdata(name=name, gender= gender,father=father,village=village,mandal=mandal,district=district,phno1=phno1, phno2= phno2,balance=0)
        if(insertdata.objects.filter(phno1=phno1).exists()):
            messages.error(request,"**phno is already exists**")
            return render(request,'details.html',{'d':d})
            #return redirect('/')
        elif(len(phno1)!=10):
            messages.error(request,"**phno1 is not a valid number**")
            return render(request,'details.html',{'d':d})
        elif(len(phno2)>0 and len(phno2)!=10):
            messages.error(request,"**phno2 is not a valid number**")
            return render(request,'details.html',{'d':d})
        else:
            var.save()
            messages.success(request,"you are sucessfully registered")
            return render(request,'details.html',{'d':d})
            #  return redirect('/')
    else:    
        return render(request,'details.html',{'d':d})
#to display product add webpage 
def toadd(request):
    return render(request,"productadd.html")
#add the product details into database
def addaproduct(request):
    d={'name':"","type":"",'price':""}
    if(request.method=="POST"):
        name=request.POST.get('name')
        print(name)
        d['name']=name
        ptype=request.POST.get('type')
        d['type']=ptype
        price=request.POST.get('price')
        d['price']=price
        var=addproduct(name=name,ptype=ptype,price=price)
        if(addproduct.objects.filter(name=name).exists()):
            messages.error(request,"productname already exists try with another")
            return render(request,'productadd.html',{'d':d})
        else:
            var.save()
            messages.success(request,"product added successfully")
            return render(request,'productadd.html',{'d':d})
    else:
        return render(request,"productadd.html",{'d':d})    
#to display product purchasing page
def product(request):
    result=addproduct.objects.values('name')
    return render(request,"purchasing.html",{'result':result})
#to adding details related to puchasing into datebase
def purchasing(request):
    result=addproduct.objects.values('name')
    d={'name':"","phno":"",'product':"","quantity":""}
    if(request.method=="POST"):
        fname=request.POST.get('name')
        d['name']=fname
        phno=request.POST.get('phno')
        d['phno']=phno
        name=request.POST.get('product')
        d['product']=name
        quantity=request.POST.get('quantity')
        d['quantity']=quantity
        date=datetime.datetime.now().date()
        var=farmerproducts(name=name,phno=phno,quantity=quantity,date=date,billgenerate=0)
        if(not insertdata.objects.filter(phno1=phno).exists()):
            messages.error(request,"**mobile no doesn't exist!**")
            return render(request,'purchasing.html',{'d':d,'result':result})
        else:
            print(name)
            var.save()
            messages.success(request,"added to cart sucessfully")
            return render(request,'purchasing.html',{'d':d,'result':result})
    else:
        return render(request,"purchasing.html",{'d':d,'result':result})
def billpayment(request):
    if(farmerproducts.objects.filter(billgenerate=0).exists()):
        query=farmerproducts.objects.filter(billgenerate=0)[:1].get()
        d={'date':"",'name':'','village':'','totalbillprice':0,'phno':''}
        date=datetime.datetime.now().date()
        d['date']=date
        r=insertdata.objects.get(phno1=query.phno)
        d['name']=r.name
        d['phno']=query.phno
        d['village']=r.village
        count=0
        query=farmerproducts.objects.filter(billgenerate=0)
        # df = pd.DataFrame(query.values())
        # print(df)
        d1=dict()
        for s in query:
            l=[]
            obj=addproduct.objects.get(name=s.name)
            l.append(count+1)
            l.append(obj.name)
            l.append(s.quantity)
            l.append(int(s.quantity)*int(obj.price))
            d['totalbillprice']=d['totalbillprice']+int(s.quantity)*int(obj.price)
            d1[count]=l
            count=count+1
        #query.update(billgenerate=1)
        return render(request,"billpayment.html",{'d':d,'d1':d1})
    else:
        messages.error(request,"select atleast one product")
        return render(request,'purchasing.html')
    return render(request,'billpayment.html')
def updatebalanceafterbill(request):
    if(request.method=="POST"):
        print(request.POST)
        phno=request.POST.get('phno')
        totalamount=request.POST.get('totalamount')
        amount=request.POST.get('amount')
        balance=int(totalamount)-int(amount)
        r=insertdata.objects.get(phno1=phno)
        balance=int(r.balance)+int(balance)
        r=insertdata.objects.filter(phno1=phno)
        r.update(balance=balance)
        query=farmerproducts.objects.filter(billgenerate=0)
        query.update(billgenerate=1)
        return render(request,'purchasing.html')
    return render(request,'billpayment.html')

def getdetails(request):
    phno=request.GET.get('phone_number')
    if(insertdata.objects.filter(phno1=phno).exists()):
        result=insertdata.objects.filter(phno1=phno).first()
        data={}
        if result:
            data={
                'name':result.name,
                'fathername':result.father,
                'balance':result.balance,
                'message':"sucesss"
            }
        return JsonResponse(data)
    else:
        data={'message':"error"}
        return JsonResponse(data)
def balance(request):
    result=insertdata.objects.all()
    return render(request,"balancepayment.html",{"result":result})
def updatebalance(request):
    result={'phno':'','name':'','father':'','balance':'','amount':'','message':''}
    if(request.method=="POST"):
        phno=request.POST.get('phno')
        result['phno']=phno
        name=request.POST.get('name')
        result['name']=name
        father=request.POST.get('father')
        result['father']=father
        balance=request.POST.get('balance')
        result['balance']=balance
        amount=request.POST.get('amount')
        result['amount']=amount
        if(int(amount)>int(balance)):
            messages.error(request,"amount to be paid is higher than balance")
            return render(request,'balancepayment.html',{'result':result})
        else:
            var=insertdata.objects.filter(phno1=phno)
            var1=insertdata.objects.get(phno1=phno)
            bal=int(balance)
            balance=int(balance)-int(amount)
            var.update(balance=balance)
            # messages.success(request,"balance was updated sucessfully")
            # message="Dear {0} you have cleared balance amount of {1} and the remaining balance is {2} .thank you".format(var1.name,bal,balance)
            # sender='+9182266198'
            # recipients=[phno]
            # send_sms(body=message, originator=sender, recipients=recipients)
            messages.success(request,"balance updated suceesfully")
            return render(request,'balancepayment.html')
    return render(request,'balancepayment.html',{'result':result})
def update(request):
    result=addproduct.objects.values('name')
    return render(request,"updateproduct.html",{"result":result})
def updateaproduct(request):
    result=addproduct.objects.values('name')
    if(request.method=='POST'):
        name=request.POST.get('old')
        newname=request.POST.get('newname')
        ptype=request.POST.get('ptype')
        price=request.POST.get('price')
        if(len(newname) or len(ptype) or len(price)):
            query=addproduct.objects.filter(name=name)
            if(len(newname)>0):
                query.update(name=newname)
            if(len(ptype)>0):
                query.update(ptype=ptype)
            if(len(price)>0):
                query.update(price=int(price))
            messages.success(request,"details are updated")
            return render(request,'updateproduct.html',{'result':result})
        else:
            messages.error(request,"**atleast one is required to update**")
            return render(request,'updateproduct.html',{'result':result})
    else:
        return render(request,'updateproduct.html',{'result':result})

def dashboard(request):
    d={'totalamount':'','amount':'','balance':'','time':''}
    table1_rows = farmerproducts.objects.all()
    total_price = 0
    for row in table1_rows:
            table2_row = addproduct.objects.get(name=row.name)
            total_price += row.quantity * table2_row.price
    d['totalprice']=total_price
    b=insertdata.objects.aggregate(Sum('balance'))['balance__sum']
    # for r in balance:
    #     tbalance=tbalance+r.balance
    d['balance']=int(b)
    result = farmerproducts.objects.values('name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    result1 = farmerproducts.objects.values('name').annotate(total_quantity=Sum('quantity')).order_by('total_quantity')[:5]
    result2=insertdata.objects.all().order_by('-balance')
    print(result)
    d['amount']=d['totalprice']-d['balance']
    d['time']=datetime.datetime.now()
    return render(request,'dashboard.html',{'d':d,'result':result,'result1':result1,'result2':result2})
   

