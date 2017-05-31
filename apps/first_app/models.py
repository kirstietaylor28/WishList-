from __future__ import unicode_literals

from django.db import models

from django.shortcuts import render

import re

class UserManager(models.Manager):
	def validate(self, POST):
		errors= []
		if len(POST['password']) < 8:
			errors.append('Password must be at least 8 characters long.')
		if POST['password'] != POST['confirm_pass']:
			errors.append('Passwords must match')
		return errors

class ItemManager(models.Manager):
	def validate(self, POST):
		errors = []
		if not POST['item']: 
			errors.append('Please enter an item name')
		if len(POST['item']) < 3:
			errors.append('Item must be more than 3 characters')
		return errors 

class User(models.Model):

	name = models.CharField(max_length= 100)
	username = models.CharField(max_length= 100)
	password = models.CharField(max_length= 16)
	objects = UserManager()

class Item(models.Model):

	item_name = models.CharField(max_length= 100)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	objects = ItemManager()

class Wishlist(models.Model):

	item = models.ManyToManyField(Item, related_name="wishlists")
	user = models.ForeignKey(User, related_name="wishlist")
	created_at = models.DateTimeField(auto_now_add=True, blank=True)






