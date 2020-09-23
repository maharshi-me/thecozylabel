from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import View
# Create your views here.

