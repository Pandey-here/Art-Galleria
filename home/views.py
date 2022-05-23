from traceback import print_tb
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from .forms import CustomerForm
from home.models import Customer
from django.contrib.auth import logout,authenticate, login as auth_login
#from models.User

# Create your views here.
def customer_support(request):
    if request.user.is_anonymous :
        return redirect('home:register')
    else :
        if request.method=='POST':
            form1=CustomerForm(request.POST,request.FILES)

            if form1.is_valid:
                temp=form1.save(commit=False)
                temp.our_user=request.user
                temp.save()

                return redirect('/')
            else:
                print(form1.errors)
                return render(request,'customer_support.html',{'message' : 'Something went wrong :('})
        else:
            form=CustomerForm()
            temp=Customer.objects.filter(our_user=request.user)
            for i in temp:
                print(i.custom_id)
            print("--------------------------------------------")
            return render(request,'customer_support.html',{'form':form, 'all_img':temp})

def register(request):
    if request.method=="POST" :
        email=request.POST['email']
        password=request.POST['password']
        username_u=request.POST['username']
        cpassword=request.POST['cpassword']

        if cpassword==password :
            try:
                user=User.objects.create_user(username=email,email=username_u,password=cpassword)
                user.save()
                return redirect('home:login')
            except Exception as e :
                print(e)
                return render(request,'register.html',{'error' : 'Data is not validated. Try Again!'})
        else:
            return render(request,'register.html',{'error' : 'Check your Password!'})
    
    return render(request,'register.html')

def login(request):
    if request.method=="POST":
        user_email=request.POST['email']
        user_password=request.POST['password']
        user=authenticate(request,username=user_email,password=user_password)

        if user is not None:
            print("==========================================")
            auth_login(request,user)
            return redirect('home:customer_support')
        else:
            print("---------------------------------------------")
            return render(request,'login.html',{'error' : 'Invalid user!'})
    else:
        print("***************************************************")
        return render(request,'login.html')



def logout_view(request):
    logout(request)
    return redirect('home:login')

# def index(request):
#     if request.method=='POST':
#         print("Fuck")
#         form1=CustomerForm(request.POST,request.FILES)

#         if form1.is_valid:
#             temp=form1.save(commit=False)
#             temp.save()
#             return redirect('/')
#         else:
#             print(form1.errors)
#             return render(request,'index.html',{'message' : 'Something went wrong :('})
#     else:
#         form=CustomerForm()
#         temp=Customer.objects.all()
#         print("--------------------------------------------")
#         return render(request,'index.html',{'form':form, 'all_img':temp})

def delete_img(request,our_key):
    if our_key:
        kgf=request.user
        ele=Customer.objects.get(our_user=kgf,custom_id=our_key)   #Get is for operating with one object filter for more than 1
        ele.delete()
        return redirect('/')
    else :
        print("Invalid Id")


def update(request,our_key):
    if our_key:
        if request.method=="POST":
            post_check=Customer.objects.get(custom_id=our_key,our_user=request.user)
            form=CustomerForm(request.POST,request.FILES,instance=post_check)
            if form.is_valid():
                form.save()
                return redirect('home:customer_support')
            else :
                print(form.errors)
                redirect('/')
        else:
            check=Customer.objects.get(custom_id=our_key,our_user=request.user)
            form=CustomerForm(instance=check)
              
            return render(request,'edit_customer_support.html',{'form':form})
    else:
        print("id doesn't exist ")