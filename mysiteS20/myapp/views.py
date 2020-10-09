'''
from datetime import datetime
from random import random
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import InterestForm, OrderForm, RegisterForm
from .models import Topic, Course, Student, Order, User
from django.shortcuts import get_list_or_404, render, redirect
from django import forms

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
'''

import string
from datetime import datetime
import random
from django.contrib.auth import (
    login as auth_login,
)
from .forms import InterestForm, OrderForm, RegisterForm, AccountForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, FormView
from .models import Topic, Course, Student, Order, User
from django.shortcuts import get_list_or_404, render, resolve_url, redirect
#from .forms import OrderForm, InterestForm, PasswordRequestForm, UserUpdateForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    if request.session.test_cookie_worked():
        print("Test cookie worked")
        request.session.delete_test_cookie()
        print("Test cookie deleted")
    else:
        print("Please enable cookies and try again.")

    top_list = Topic.objects.all().order_by('id')[:5]
    course_list = Course.objects.all().order_by('-price')[:5]
    lst_login = ''
    if 'last_login' in request.session:
        lst_login = request.session.get('last_login')
    else:
        HttpResponse("Your last login was more than one hour ago")
    return render(request, 'myapp/index.html',
                  {'top_list': top_list, 'course_list': course_list, 'lst_login': lst_login})

    # Answer 2.C - Yes, we're passing course_list as 2nd context variable to display the top 5 courses
    # which have the highest price in descending order and whether a particular course is available
    # for everyone or not.


def about(request):
    request.session.set_test_cookie()

    # Number of visits to this view, as counted in the session variable.
    about_visits = request.session.get('about_visits', 0)
    request.session['about_visits'] = about_visits + 1
    request.session.set_expiry(300)
    return render(request, 'myapp/about.html', {'about_visits': about_visits})


# 4.C No, we are not passing any context variable here.
# 4.D Not Applicable


def detail(request, top_no):
    get_list_or_404(Topic, id=top_no)
    tp = Topic.objects.get(id=top_no)
    courses = Course.objects.filter(topic=top_no)
    return render(request, 'myapp/detail.html', {'tp': tp, 'courses': courses})


# 5.C we are passing 2 context variables.
# 5.D we are passing tp as variable for Topic model  and courses as a variable for Course model.

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def placeorder(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
             order = form.save(commit=False)
        #     if order.levels <= order.course.stages:
        #         if order.course.price > 150:
        #             updated_price = order.course.discount()
        #             print(updated_price)
        #             order.discounted_price = updated_price
             order.save()
             msg = 'Your course has been ordered successfully.'
        else:
             msg = 'You exceeded the number of levels for this course.'
        return render(request, 'myapp/order_confirmation.html/', locals())
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html/', {'form': form, 'msg': msg, 'courlist': courlist})


def coursedetail(request, cour_id):
    msg = ''
    course = Course.objects.get(id=cour_id)
    # course_list = Course.objects.all().order_by('-price')[:5]
    # top_list = Topic.objects.all().order_by('id')[:10]
    if request.method=='GET':
        form=InterestForm()
        msg='Courses'
        return render(request, 'myapp/coursedetail.html', {'form':form, 'course':course})
    else:
     if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            obj= form.cleaned_data['interested']
            if obj=='Yes':
                course.interested = course.interested + 1
                course.save()
                top_list = Topic.objects.all().order_by('id')[:10]
                return render(request, 'myapp/index.html', {'top_list': top_list, 'course_list': course_list})
            else:
                msg="You are not interested in this course!"
            return render(request, 'myapp/coursedetail.html', {'form':form, 'course':course, 'msg':msg})
     else:
        form = InterestForm()
        msg="Please select a valid option!"
     return render(request, 'myapp/coursedetail.html', {'form': form, 'course': course, 'msg':msg})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                current_login = datetime.now()
                request.session['last_login'] = current_login.strftime("%d-%m-%Y %H:%M:%S")
                request.session.set_expiry(3600)
                request.session.get_expire_at_browser_close()

                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    request.session.flush()
    return render(request, 'myapp/logout.html')

def profile_image(request):
    if (request.method == 'POST'):
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()
            return render(request, 'myapp/index.html', {'form':form})
    else:
        form = AccountForm()
    return render(request, 'myapp/upload_photo.html', {'form': form})

#@login_required
def myaccount(request):
    sid = Student.objects.filter(id=request.user.id)


    #sid = Student.objects.get(name=request.user.username)
    #print(sid)
    if sid:
        #print(Student.picture.path)
        firstname = request.user.first_name
        lastname = request.user.last_name
        interest_list = sid.values_list('interested_in__name')
        print(interest_list)
        order_list = sid.values_list('order__course__name')
        print(order_list)
        # context = {'First_name': firstname, 'Last_name': lastname, 'interest_list': interest_list,
        #            'order_list': order_list}
        return render(request, 'myapp/myaccount.html', {'First_name': firstname, 'Last_name': lastname, 'interest_list': interest_list, 'order_list': order_list})
    else:
        context = "You are not a registered student!"
        return render(request, 'myapp/login.html', {'context':context})

def success(request):
 return render(request, 'myapp/myaccount.html')
 #return HttpResponse('Successfully Uploaded')


def register(response):
    student= Student.objects.all()
    if(response.method=='POST'):
        form=RegisterForm(response.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            form.save()
            return redirect('myapp:index')
    else:
        form=RegisterForm()
    return render(response, 'myapp/register.html', {'form': form, 'student': 'student'})


