from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from .models import User, Wishlist, Item

import bcrypt

def index(request):
	context = {
		"users" : User.objects.all()
	}
	return render(request, 'first_app/index.html')

def register(request):
	if request.method == "POST":
		information = request.POST
		errors = User.objects.validate(information)
		if errors:
			for error in errors:
				messages.error(request, error)
				return redirect('/')
		else:
			hashed_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name= request.POST['name'], username=request.POST['username'], password=hashed_pass)
			wishlist = Wishlist.objects.create(user=user)
			request.session['user'] = user.id
			print wishlist
			return redirect('/wishlist')
	else:
		return redirect('/')

def login(request):
	if request.method == "POST":
		user = User.objects.filter(username=request.POST['login_username'])
		hashed_pass = bcrypt.hashpw(request.POST['login_password'].encode(), user[0].password.encode())
		if user:
			user = user[0]
			if user.password != hashed_pass:
				messages.error(request, 'Password is incorrect')
				return redirect('/')
			else:
				request.session['user'] = user.id
				return redirect('/wishlist')
		else:
			messages.error(request, 'Username does not exist.')
			return redirect('/')

def wishlist(request):

	context = {
		'user' : User.objects.get(id=request.session['user']),
        'wishlist' : Wishlist.objects.filter(user=User.objects.get(id=request.session['user']))
	}

	return render(request, 'first_app/wishlist.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')

def create (request):
	return render(request, 'first_app/create.html')

def add (request):
	if request.method == "POST":
		new_item = request.POST
		errors = Item.objects.validate(new_item)
		if errors:
				for error in errors:
					messages.error(request, error)
					url_redirect = request.META['HTTP_REFERER']
					return redirect(url_redirect)
		else:
			add_item = request.POST['item']
			this_item = Item.objects.create(item_name=add_item)
			this_wishlist= Wishlist.objects.get(user=request.session['user'])
			this_wishlist.item.add(this_item)
			return redirect('/wishlist')

def item(request, id):
	item = Item.objects.get(id=id)
	print item.item_name
	context = {
		'item' : item,
		'wishlist' : Wishlist.objects.filter(item=item),
	}
	return render(request, 'first_app/item.html', context)

def remove(request, id):
	delete_item = Item.objects.get(id = id).delete()
	return redirect('/wishlist')



