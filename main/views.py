from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.decorators import login_required
import datetime

@login_required(login_url='/login')

def show_main(request):
    products = Product.objects.filter(user=request.user) # fetch all Product object from the application's database

    context = {
        'name': request.user.username,
        # 'name': 'Tiva Adhisti Nafira Putri', # Your name
        'class': 'PBP KI', # Your PBP Class
        'products': products,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)


# add a new product when the form is submitted
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('main:show_main'))


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# return data in XML format
# This function accepts a request as the parameter.
# Create a variable to store all fetched Product objects.
def show_xml(request):
    data = Product.objects.all()
    # return the previously fetched data as XML
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


# return data in JSON format
def show_json(request):
    data = Product.objects.all()
    # return the previously fetched data as JSON
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")



# Retrieving Data Based on ID in XML and JSON Formats
def show_xml_by_id(request, id):
    # store the query result of data with a specific ID from the Product model
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
def show_json_by_id(request, id):
    # store the query result of data with a specific ID from the Product model
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

