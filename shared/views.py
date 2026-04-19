from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView 
# Create your views here.

class HomepageView(TemplateView):
    template_name = "shared/home.html"
