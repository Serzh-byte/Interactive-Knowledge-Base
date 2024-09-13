from django.shortcuts import render, redirect
from django import forms

def index(request):
    return render(request, "knowledge_base/home.html", {
    })