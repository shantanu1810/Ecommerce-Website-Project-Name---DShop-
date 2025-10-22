from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from DShop.models import *
from DShop.forms import productsadd
import re
from django.core.files.storage import FileSystemStorage
import smtplib
from email.message import EmailMessage
import datetime
#Global variable to manage customers

logined_users=dict({})
logined_owner=dict({})

def contactus(request):
    return render(request,'contactus.html')

def help(requests):
    return render(requests,'help.html')

def about(request):
    return render(request,'aboutus.html')

def home(requests):
    if(requests.method=='POST'):
        sea=requests.POST.get('searchitem')
        if(sea != None):
            return redirect("/search="+sea,search=sea)
        sea=requests.POST.get('products_types')
        if(sea!=None):
            return redirect('/search='+sea,search=sea)
        sea=requests.POST.get('offers')
        if(sea!=None):
            return render(requests,'offers.html')
        sea=requests.POST.get('shop')
        if(sea!=None):
            return redirect('/search='+sea,search=sea)
        sea=requests.POST.get('price')
        if(sea!=None):
            return redirect('/search='+sea,search=sea)
        sea=requests.POST.get('Trending')
        if(sea!=None):
            return redirect('/search='+sea,search=sea)
        sea=requests.POST.get('brand')
        if(sea!=None):
            sea+=" brand"
            return redirect('/search='+sea,search=sea)
        
    return render(requests,"HomePage.html")

def wos_search(request,search):
    if(request.method=='POST'):
        pid=request.POST.get('productid')
        obj=Products.objects.get(product_id=pid)
        return render(request,'Product_page_wos.html',{'product':obj})
    products=[]
    pro=Products.objects.all()
    for i in pro:
        if(search=="shop"):
            products.append(i)
            continue
        if(search=="Less Cost Products" and int(i.price)<200):
            products.append(i)
            continue
        if(search=='brand' and re.search(search,i.brand)):
            products.append(i)
            continue
        if(re.search(search,i.name) or re.search(search,i.sub_type) or re.search(search,i.product_type)):
            products.append(i)
    message=""
    if 'brand' in search:
        message="Products Display Based on Brand - "+search
    elif search=='Less Cost Products':
        message="Products Display based on less price."
    elif search!='shop':
        message="Search result based on '"+search+"'"
    return render(request,"searchpage_withouthome.html",{'products':products,'search':search,'message':message})

def details(request,id):
    global logined_users
    if(request.method=="POST"):
        user=Customers.objects.get(id=id)
        name=request.POST.get('name')
        if(name!=None and name!=""):
            user.customer_name=name
        Phone=request.POST.get('phone')
        if(Phone!=None and Phone!=""):
            user.phone_no=Phone
        al_email=request.POST.get('altemail')
        if(al_email!=None and al_email!=""):
            user.alternate_email=al_email
        ap=request.POST.get("altphone")
        if(ap!=None and ap!=""):
            user.alternate_no=ap
        user.save()
        user=Customers.objects.get(id=id)
        logined_users[id]=user
        
    return render(request, 'customer_details.html',{'user':logined_users[id]})

def orders(request,id):
    if(request.method=='POST'):
        pid=request.POST.get('prdt0')
        quant=request.POST.get('prdt1')
        price=request.POST.get('prdt2')
        pay=request.POST.get('prdt3')
        status=request.POST.get('prdt4')
        date=request.POST.get('prdt5')
        op=request.POST.get('operation')
        address=request.POST.get('prdt6')
        search=pid+" "+quant+" "+price+" "+pay+" "+status+" "+date+" "+address
        p=Products.objects.get(product_id=pid)
        user=Customers.objects.get(id=id)
        if(op=='feedback'):
            rating=request.POST.get('rating')
            feed=request.POST.get('feedback')
            message=rating+" "+feed
            p.feedback_rating.append(message)
            p.ratings.append(int(rating))
            p.average_rating=round(sum(p.ratings)/len(p.ratings),1)
            p.people_rate=str(int(p.people_rate)+1)
            p.save()
            search=pid+" "+quant+" "+price+" "+pay+" "+status+" "+date+" "+address
            indx=user.order.index(search)
            user.order[indx]=pid+" "+quant+" "+price+" "+pay+" f "+date+" "+address
            user.save()
            logined_users[id]=user
        elif(status=='otw' or status=='release'):
            search=pid+" "+quant+" "+price+" "+pay+" "+status+" "+date+" "+address
            indx=user.order.index(search)
            user.order[indx]=pid+" "+quant+" "+price+" "+pay+" c1 "+date+" "+address
            p.order_quantity[str(id)+" "+date]=quant+" "+price+" "+pay+" c1 "+address
            p.new_order=str(int(p.new_order)-1)
            user.save()
            p.save()
            logined_users[id]=user
    products=[]
    details=[]
    user=Customers.objects.get(id=id)
    for i in user.order:
        l=list(i.split(' '))
        if(Products.objects.get(product_id=l[0])):
            products.append(Products.objects.get(product_id=l[0]))
        else:
            user.order.remove(i)
        details.append(l)
    user.save()
    user=Customers.objects.get(id=id)
    logined_users[id]=user
    prodet=zip(products,details)
    return render(request,"Customer_order.html",{'products':prodet,'user':logined_users[id]})

pass_change_request=dict({})

def password_forget(request):
    if(request.method=="POST"):
        subject="Password Change request !"
        body="Your one time password is "+str(p)
        
        msg=EmailMessage()
        msg.set_content(body)
        msg['subject']=subject
        msg['to']=to
    
        user="exampleemailforalertsystem123@gmail.com"
        password="caxitxlsynsvldct"
        msg['from']=user
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(user,password)
        server.send_message(msg)
        server.quit()
def passwordchange(request,id):
    if(request.method=='POST'):
        cust=Customers.objects.get(id=id)
        oldpass=request.POST.get('oldpass')
        newpass=request.POST.get('newpass')
        againnewpass=request.POST.get('againnewpass')

        if(oldpass!=cust.password):
            return render(request,'password_change.html',{'user':logined_users[id],'messagef':"Failed to change Password , Old Password is not Matching",'messages':""})
        elif(newpass!=againnewpass):
            return render(request,'password_change.html',{'user':logined_users[id],'messagef':"Failed to change Password",'messages':""})
        else:
            cust.password=newpass
            cust.save()
            logined_users[id]=cust
            return render(request,'password_change.html',{'user':logined_users[id],'messagef':"",'messages':"Password Change Successfully"})
    return render(request,'password_change.html',{'user':logined_users[id],'messagef':"",'messages':""})
def feedback(request,id):
    if(request.method=="POST"):
        try:
            subject="Customer Feedback / Issue related query"
            query=request.POST.get('query')
            print(query)
            body="Customer name -- "+logined_users[id].name+"\n Customer ID -- "+id+"\nEmail -- "+logined_users[id].email+"\n\n\nQuery -- "+query
            msg=EmailMessage()
            msg.set_content(body)
            msg['subject']=subject
            msg['to']="exampleemailforalertsystem123@gmail.com"
            user="exampleemailforalertsystem123@gmail.com"
            password="caxitxlsynsvldct"
            msg['from']=user
            server=smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(user,password)
            server.send_message(msg)
            server.quit()
            return render(request,"feedback.html",{'user':logined_users[id],"messages":'Message Send Successsfully. We will contact you shortly. Thank you!!','messagef':""})
        except :
            return render(request,"feedback.html",{'user':logined_users[id],"messagef":'Message Failed to Send.','messages':""})
    return render(request,"feedback.html",{'user':logined_users[id],"messages":'','messagef':""})

def offers(request,id):
    gifts=[]
    for i in logined_users[id].gifts:
        gif=Offer_Gifts.objects.get(OfferID=i)
        gifts.append(gif)
    return render(request,'gift_card.html',{'user':logined_users[id],'gifts':gifts})


def addressupdate(request,id):
    if(request.method=='POST'):
        user=Customers.objects.get(id=id)
        road=request.POST.get('road')
        area=request.POST.get('area')
        house=request.POST.get('house')
        state=request.POST.get('state')
        city=request.POST.get('city')
        pin=request.POST.get('pin')
        addre=""
        if(road!=""):
            addre+=road+", "
        if(area!=""):
            addre+=area+", "
        if(house!=""):
            addre+=house+", "
        if(road!=""):
            addre+=road+", "
        if(state!=""):
            addre+=state+", "
        if(city!=""):
            addre+=city+", "
        if(pin!=""):
            addre+=pin+""
        user.Address=addre
        user.save()
        logined_users[id]=user
        
    return render(request,'customeraddressset.html',{'user':logined_users[id]})

def signingin(requests):
    if(requests.method=='POST'):
        check=requests.POST.get('Bussiness_account')
        global logined_users
        if(not check=='on'):
            user=requests.POST.get('username_login')
            password=requests.POST.get('password')
            user_valid=Customers.objects.filter(username=user)
            user_valid_email=Customers.objects.filter(email=user)
            if(user_valid.exists()):
                user_data=Customers.objects.get(username=user)
                if(user_data.password==password):
                    global logined_users
                    logined_users[user_data.id]=user_data
                    return redirect("/home/"+str(user_data.id),id=user_data.id)
            elif(user_valid_email.exists()):
                user_data=Customers.objects.get(email=user)
                if(user_data.password==password):
                    logined_users[user_data.id]=user_data
                    return redirect("/home/"+str(user_data.id),id=user_data.id)
        else:
            user=requests.POST.get('username_login')
            password=requests.POST.get('password')
            user_valid=Bussiness.objects.filter(bussiness_name=user)
            user_valid_email=Bussiness.objects.filter(bussiness_email=user)
            if(user_valid.exists()):
                user_data=Bussiness.objects.get(bussiness_name=user)
                if(user_data.password==password):
                    logined_owner[user_data.id]=user_data
                    return redirect("/bussinessPage/"+str(user_data.id),id=user_data.id)
            elif(user_valid_email.exists()):
                user_data=Bussiness.objects.get(bussiness_email=user)
                if(user_data.password==password):
                    logined_owner[user_data.id]=user_data
                    return redirect("/bussinessPage/"+str(user_data.id),id=user_data.id)
    return render(requests,'signin.html')


@csrf_protect
def create_account(requests):
    if(requests.method=='POST'):
        acc_type=requests.POST.get('account')
        if(acc_type=='Personal'):
            username=requests.POST.get('username')
            email=requests.POST.get('email')
            password=requests.POST.get('password')
            customer=Customers()
            customer.gifts.append('1')
            customer.gifts.append('2')
            customer.alternate_email=""
            customer.alternate_no=""
            customer.Address=""
            customer.customer_name=""
            customer.phone_no=""
            customer.username=username
            customer.email=email
            customer.password=password
            customer.save()
            return render(requests,'signin.html')
        else:
            username=requests.POST.get('bussinessname')
            email=requests.POST.get('email')
            password=requests.POST.get('password')
            bussiness=Bussiness()
            bussiness.bussiness_name=username
            bussiness.bussiness_email=email
            bussiness.password=password
            bussiness.no_of_products=str(0)
            bussiness.save()
            return render(requests,'signin.html')
    return render(requests,'create_account.html')


def customer_home(request,id):
    global logined_users
    if(request.method=='POST'):
        r=request.POST.get('requesting')
        if(r=='logout'):
            print(r," ",logined_users[id])
            del logined_users[id]
            return redirect('/')
        r=request.POST.get('search')
        if(r!=None):
            return redirect("/home/"+str(id)+"/search"+r+"/",id=id,searchvalue=r)
        r=request.POST.get('searchbytype')
        if(r!=None):
            return redirect('/home/'+str(id)+"/search"+r+'/',id=id,searchvalue=r)
    if(id in logined_users):
        return render(request,'customer_homepage.html',{'user':logined_users[id]})

def product_order(request,id,pid):
    product=Products.objects.get(product_id=pid)
    if(request.method=='POST'):
        cid=request.POST.get('cid')
        op=request.POST.get('operation')
        date=request.POST.get('dt')
        quantity=request.POST.get('quantity')
        total=request.POST.get('total')
        pay=request.POST.get('pay')
        status=request.POST.get('status')
        address=request.POST.get('address')
        print(address)
        search=pid+" "+quantity+" "+total+" "+pay+" "+status+" "+date+" "+address
        user=Customers.objects.get(id=cid)
        if(op=="confirm"):
            indx=user.order.index(search)
            user.order[indx]=pid+" "+quantity+" "+total+" "+pay+" A "+date+" "+address
            user.save()
            if(product.new_order!="0"):
                product.new_order=str(int(product.new_order)-1)
            search=cid+" "+date
            product.order_quantity[search]=quantity+" "+total+" "+pay+" A"+" "+address
            product.save()
        elif(op=='cancel'):
            indx=user.order.index(search)
            user.order[indx]=pid+" "+quantity+" "+total+" "+pay+" c2 "+date+" "+address
            user.save()
            if(product.new_order!="0"):
                product.new_order=str(int(product.new_order)-1)
            search=cid+" "+date
            product.order_quantity[search]=quantity+" "+total+" "+pay+" c2"+" "+address
            product.save()
        else:
            indx=user.order.index(search)
            user.order[indx]=pid+" "+quantity+" "+total+" "+pay+" d "+date+" "+address
            user.save()
            search=cid+" "+date
            product.order_quantity[search]=quantity+" "+total+" "+pay+" d"+" "+address
            product.people_buy=str(int(product.people_buy)+1)
            product.save()

    new_orders=[]
    cancel_order=[]
    complete=[]
    ongoing=[]
    newcid=[]
    cancelcid=[]
    completeid=[]
    onid=[]
    for key in product.order_quantity:
        l=list(product.order_quantity[key].split(' '))
        k=list(key.split(' '))
        if(l[3]=='otw'):
            new_orders.append(l)
            newcid.append(k)
        elif(l[3]=='c1' or l[3]=='c2'):
            cancel_order.append(l)
            cancelcid.append(k)
        elif(l[3]=='d'):
            complete.append(l)
            completeid.append(k)
        else:
            ongoing.append(l)
            onid.append(k)
    new=zip(new_orders,newcid)
    cancel=zip(cancel_order,cancelcid)
    ongo=zip(ongoing,onid)
    completed=zip(complete,completeid)
    return render(request,'handle_order.html',{'owner':logined_owner[id],'product':product,'new':new,'cancel':cancel,'completed':completed,'ongo':ongo,'n':new_orders,'c':complete,'can':cancel_order,'o':ongoing,'pid':pid})

def bussiness_product_managing(request,id):
    global logined_owner
    if(id in logined_owner):
        if(request.method=='POST'):
            pid=request.POST.get('pid')
            return redirect('/bussinessPage/'+str(id)+'/ProductsOrderStatus/productid'+pid+"/manage",id=id,pid=pid)
        pro=[]
        for i in logined_owner[id].products:
            pro.append(Products.objects.get(product_id=i))
        return render(request,'bussiness_product_order.html',{'owner':logined_owner[id],'products':pro})

def bussiness_page(request,id):
    global logined_owner
    if(id in logined_owner):
        if(request.method=='POST'):
            re=request.POST.get('requesting')
            if(re=='logout'):
                del logined_owner[id]
                return redirect('/')
            
        return render(request,'bussiness_homepage.html',{'owner':logined_owner[id]})
    
def bussiness_product_rating(request,id):
    global logined_owner
    if(id in logined_owner):
        if(request.method=='POST'):
            pid=request.POST.get('pid')
            return redirect('/bussinessPage/'+str(id)+"/Products=rating/"+pid,id,pid)
        pro=[]
        for i in logined_owner[id].products:
            pro.append(Products.objects.get(product_id=i))
        return render(request,'bussiness_product_rating.html',{'owner':logined_owner[id],'products':pro})
    
def bussiness_product_allfeed(request,id,pid):
    product=Products.objects.get(product_id=pid)
    feed=[]
    for i in product.feedback_rating:
        print(i)
        feed.append(i)
    return render(request,'allfeedback_on_product.html',{'feed':feed,'product':product})

def bussiness_page_details(request,id):
    global logined_owner
    if(id in logined_owner):
        if request.method=="POST":
            name=request.POST.get('ownername')
            phone=request.POST.get('phoneno')
            addr=request.POST.get('address')
            cust=Bussiness.objects.get(id=id)
            cust.owner_name=name
            cust.phone_no=phone
            cust.Address=addr
            cust.save()
            logined_owner[cust.id]=cust
        return render(request,'Bussiness_details_page.html',{'owner':logined_owner[id],"message_success":"","message_fail":""})
    

def bussiness_page_addproduct(request,id):
    global logined_owner
    if(id in logined_owner):
        if request.method=="POST":
            name=request.POST.get('name')
            price=request.POST.get('price')
            description=request.POST.get('description')
            product_type=request.POST.get('product_type')
            brand=request.POST.get('brand')
            stype=request.POST.get('sub_type')
            image=request.FILES['p_image']
            owner=Bussiness.objects.get(id=id)
            new_pro=Products()
            new_pro.name=name
            new_pro.price=price
            new_pro.description=description
            new_pro.brand=brand
            new_pro.sub_type=stype
            new_pro.product_type=product_type
            new_pro.image=image
            number=int(owner.no_of_products)
            number+=1
            pid=str(int(id)*10000+number)+owner.phone_no[5:10]
            new_pro.product_id=pid
            owner.products.append(pid)
            owner.no_of_products=str(number)
            owner.save()
            new_pro.save()
            owner=Bussiness.objects.get(id=id)
            logined_owner[id]=owner
            return render(request,'AddProductsinDB.html',{'owner':logined_owner[id],"message_success":"Successfully Added","message_fail":""})
        else:
            return render(request,'AddProductsinDB.html',{'owner':logined_owner[id],"message_success":"","message_fail":""})


def searching_page(request,id,searchvalue):
    if(request.method=="POST"):
        pid=request.POST.get('productid')
        if(pid!=None):
            obj=Products.objects.get(product_id=pid)
            return render(request,'Product_page.html',{'product':obj,'user':logined_users[id],'search':searchvalue,'add':""})
        operation=request.POST.get('operation')
        if(operation=="add"):
            user=Customers.objects.get(id=id)
            user.cart.append(request.POST.get('proid'))
            user.save()
            logined_users[id]=Customers.objects.get(id=id)
            obj=Products.objects.get(product_id=request.POST.get('proid'))
            return render(request,'Product_page.html',{'product':obj,'user':logined_users[id],'search':searchvalue,'add':"Successfully Added to Cart"})
        else:
            pid=request.POST.get('proid')
            return redirect("/home/"+str(id)+"/purchase/"+pid,id,pid)
    products=[]
    pro=Products.objects.all()
    if(searchvalue=="all"):
        for i in pro:
            if(int(i.price)<150):
                products.append(i)
    else:
        for i in pro:
            if(re.search(searchvalue,i.name) or re.search(searchvalue,i.product_type) or re.search(searchvalue,i.sub_type)):
                products.append(i)

    return render(request,'searchpage.html',{'user':logined_users[id],'searchvalue':searchvalue,'products':products})

def bussiness_page_product(request,id):
    owner=logined_owner[id]
    pro=[]
    for i in owner.products:
        pro.append(Products.objects.get(product_id=i))
    return render(request,'bussiness_all_products.html',{'owner':logined_owner[id],'products':pro})

def bussiness_issue(request,id):
    if(request.method=="POST"):
        try:
            subject="Owner Issue related Query"
            query=request.POST.get('query')
            body="Owner name -- "+logined_owner[id].owner_name+"\nBussiness name -- "+logined_owner[id].bussiness_name+"\nCustomer ID -- "+id+"\nEmail -- "+logined_owner[id].bussiness_email+"\nPhone No. -- "+logined_owner[id].phone+"\n\n\nQuery -- "+query
            msg=EmailMessage()
            msg.set_content(body)
            msg['subject']=subject
            msg['to']="exampleemailforalertsystem123@gmail.com"
            user="exampleemailforalertsystem123@gmail.com"
            password="caxitxlsynsvldct"
            msg['from']=user
            server=smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(user,password)
            server.send_message(msg)
            server.quit()
            return render(request,"issueandproblem.html",{'owner':logined_owner[id],"messages":'We will contact you shortly and try to solve your problem as  early as possible. Thank you sir/madam.','messagef':""})
        except :
            return render(request,"issueandproblem.html",{'owner':logined_owner[id],"messagef":'Message Failed to Send.','messages':""})
    return render(request,"issueandproblem.html",{'owner':logined_owner[id],"messages":'','messagef':""})

def bussiness_change_price(request,id):
    if(request.method=="POST"):
        new=request.POST.get('newprice')
        pid=request.POST.get('productid')
        if(new !=" " and new!=None):
            obj=Products.objects.get(product_id=pid)
            obj.price=new
            obj.save()
    owner=logined_owner[id]
    products=[]
    for i in owner.products:
        print(i)
        products.append(Products.objects.get(product_id=i))
    return render(request,'product_price.html',{'products':products,'owner':logined_owner[id]})

def bussiness_discount(request,id):
    if(request.method == "POST"):
        new=request.POST.get('discount')
        pid=request.POST.get('productid')
        if(new !=" " and new!=None):
            obj=Products.objects.get(product_id=pid)
            obj.discount=new
            obj.save()
    owner=logined_owner[id]
    products=[]
    for i in owner.products:
        products.append(Products.objects.get(product_id=i))
    return render(request,'discount_products.html',{'products':products,'owner':logined_owner[id]})

def bussiness_product_remove(request,id):
    owner=Bussiness.objects.get(id=id)
    if(request.method == 'POST'):
        do=request.POST.get('operation')
        print(do)
        if(do=="delete"):
            print("delete")
            pid=request.POST.get('proid')
            obj=Products.objects.get(product_id=pid)
            owner.products.remove(pid)
            owner.save()
            obj.delete()
            owner=Bussiness.objects.get(id=id)
            logined_owner[id]=owner
        else:
            pid=request.POST.get('productid')
            print(pid)
            if(pid!=None):
                obj=Products.objects.get(product_id=pid)
                return render(request,"delete_confirm.html",{'owner':owner,'product':obj})
    owner=Bussiness.objects.get(id=id)
    logined_owner[id]=owner
    products=[]
    for i in owner.products:
        products.append(Products.objects.get(product_id=i))
    return render(request,'delete_product.html',{'products':products,'owner':logined_owner[id]})

def delete_confirmation(request,id):
    owner=Bussiness.objects.get(id=id)
    if(request.method=="POST"):
        do=request.POST.get('operation')
        print(do)
        if(do=="delete"):
            print("delete")
            pid=request.POST.get('productid')
            obj=Products.objects.get(product_id=pid)
            owner.products.remove(pid)
            owner.save()
            obj.delete()
            owner=Bussiness.objects.get(id=id)
            logined_owner[id]=owner
        return redirect("bussinessPage/"+str(id)+"/remove",id=id)
    
def purchase(request,id,pid):
    product=Products.objects.get(product_id=pid)
    gifts=[]
    if(request.method=='POST'):
        total=request.POST.get('finalamount')
        quantity=request.POST.get('qua')
        gift=request.POST.get('offerid')
        address=request.POST.get('address')
        print(total,"  ",quantity," ",gift," ",address)
        if(gift == ""):
            return render(request,'payment_options.html',{'user':logined_users[id],'product':product,'totalamount':total,'quantity':quantity,'gift':gift,'address':address})
        else:
            user=Customers.objects.get(id=id)
            user.gifts.remove(gift)
            return render(request,'payment_options.html',{'user':logined_users[id],'product':product,'totalamount':total,'quantity':quantity,'gift':gift,'address':address})
    for i in logined_users[id].gifts:
        g=Offer_Gifts.objects.get(OfferID=i)
        gifts.append(g)
    return render(request,'purchase_confirmation.html',{'user':logined_users[id],'product':product,"gifts":gifts})

def cart(request,id):
    if(logined_users[id]==None):
        return None
    if(request.method=='POST'):
        op=request.POST.get('operation')
        if(op!=None):
            user=Customers.objects.get(id=id)
            user.cart.remove(op)
            user.save()

        op=request.POST.get('buyproduct')
        if(op!=None):
            return redirect("/home/"+str(id)+"/purchase/"+op,id=id,pid=op)
    products=[]
    user=Customers.objects.get(id=id)
    logined_users[id]=user
    for i in user.cart:
        products.append(Products.objects.get(product_id=i))
    
    return render(request,'customer_cart.html',{'products':products,'user':logined_users[id]})

def confirmed(request,id,pid):
    if(request.method=='POST'):
        date=datetime.datetime.now()
        product=Products.objects.get(product_id=pid)
        user=Customers.objects.get(id=id)
        quantity=request.POST.get('quant')
        total=request.POST.get('totalamount')
        address=request.POST.get('address')
        print(address)

        user.order.insert(0,pid+" "+quantity+" "+total+" cash otw "+str(date)+" "+address)
        gift=request.POST.get('gift')
        if(gift!="" and gift!=None):
            user.gifts.remove(gift)
        user.save()
        key =str(id)+" "+str(date)
        product.order_quantity[key]=quantity+" "+total+" cash otw "+address
        x=int(product.new_order)
        x+=1
        product.new_order=str(x)
        product.save()
        logined_users[id]=user
        return render(request,'successfully_orderplace.html',{"user":logined_users[id],"success":product.name+" is order placed success fully your order reached to you within 3 days."})

        