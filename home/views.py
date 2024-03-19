from multiprocessing import AuthenticationError
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth  import authenticate,  login, logout
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from home.models import Contact
from home.models import Order
from django.core.mail import send_mail
import random
# Create your views here.
def home(request):
    return render(request,'home.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST['email']
        message = request.POST['message']
        ins = Contact(email=email, name=name,message=message )
        ins.save()

        print('The data has been written to the db')
        print(name, email,message)
        send_mail(
    "Verification mail",
    "Here we are , please tell us your views.",
    "aadityamohit0308@gmail.com",
    ["aadityapanday0308@gmail.com"],
    fail_silently=False,
)

    return render(request,"contact.html")


def about(request):
    return render(request,'about.html')
def service(request):
    return render(request,'service.html')
def pureveg(request):
    return render(request,'pureveg.html')
def meat(request):
    return render(request,'meat.html')
def dairy(request):
    return render(request,'dairy.html')



def signup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for erroneous input
        if len(username) < 10:
            return HttpResponseBadRequest("Your username must be at least 10 characters long.")

        if not username.isalnum():
            return HttpResponseBadRequest("Username should only contain letters and numbers")

        if pass1 != pass2:
            return HttpResponseBadRequest("Passwords do not match , make sure to add same password inside of password and confirm password")
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")
            print("Username already exists")
            return redirect('home')
        
        # Create the user
        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            send_mail(
                "Account Creation Confirmation",
                "Your account has been successfully created., Now make login ",
                "aadityamohit0308@gmail.com",  # Change to your sender email address
                [email],  # Send to the user's email address
                fail_silently=False,
            )
            print([email
                   ])
            messages.success(request, "Your account has been successfully created")
            return redirect('home')
            messages.success(request, "Your account has been successfully created")
            return redirect('home')
        except IntegrityError:
            messages.error(request, "An error occurred while creating your account. Please try again later.")
            return redirect('home')

    return render(request, 'signup.html')
def login(request):
    if request.method == 'POST':
        if 'otp' in request.POST:  # Check if OTP is being submitted
            entered_otp = request.POST['otp']
            stored_otp = request.session.get('otp')
            if stored_otp == entered_otp:
                # OTP matches, log in the user
                user_id = request.session.get('user_id')
                user = User.objects.get(id=user_id)
                auth_login(request, user)
                del request.session['otp']
                del request.session['user_id']
                return redirect('home')
            else:
                # Invalid OTP, display error
                return HttpResponse("Invalid OTP. Please try again.")
        else:
            # Regular login attempt
            loginusername = request.POST['loginusername']
            loginpassword = request.POST['loginpass']

            user = authenticate(request, username=loginusername, password=loginpassword)
            if user is not None:
                # Generate OTP
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                request.session['otp'] = otp
                request.session['user_id'] = user.id

                # Send OTP to the user's email
                send_mail(
                    "Login OTP",
                    f"Your OTP for login is: {otp}",
                    "aadityamohit0308@gmail.com",
                    [user.email],
                    fail_silently=False,
                )
                print({otp})
                # Render the OTP entry form
                return render(request, 'login.html', {'otp_required': True})
            else:
                # Invalid credentials, display error
                return HttpResponse("Invalid username or password")
        
    return render(request, 'login.html', {'otp_required': False})


def logout(request):
    auth_logout(request)
    print('logout')
    return redirect('home')

def thank(request):
    return render(request,'thank.html')

def cashondelivery(request):
    name = request.GET.get('name')
    price = request.GET.get('price')
    request.session['price'] = price  # Store price in session
    request.session['name'] = name  # Store product name in session

    
    return render(request, 'cashondelivery.html',{'name': name, 'price': price})
def cashpay(request):
    if request.method == "POST":
        # Get the post parameters
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        state = request.POST.get('state')
        city = request.POST.get('city')
        price = request.POST.get('price')
        landmark = request.POST.get('landmark')
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        order = Order.objects.create(
            name=name,
            address=address,
            phone=phone,
            email=email,
            state=state,
            city=city,
            price=price,
            landmark=landmark
        )
        send_mail(
            f"New Order: {name}",
            f"your order has been confirmed and will be delivered to you between 4-5 business days "
            f"Your order has been confirmed of :\n\nProduct: {name}\nPrice: {price}\n\nAddress: {address}\nCity: {city}\nState: {state}\nLandmark: {landmark}\n\nPhone: {phone}\nEmail: {email}\nOTP: {otp}",
            "aadityamohit0308@gmail.com",  # Replace with your email address
            [request.user.email],  # Send to the user's email address
            fail_silently=False,
        )
        return redirect('thank')
        # Here you can proceed with further processing or validation

    price = request.session.get('price')  # Retrieve price from session
    name = request.session.get('name')  # Retrieve product name from session
    return render(request, 'cashpay.html', {'name': name, 'price': price})
