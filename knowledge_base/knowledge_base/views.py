# views.py
from django.shortcuts import render, redirect, Http404
from django import forms
from . import utils


def index(request):
    return render(request, "knowledge_base/home.html", {
        'entries': utils.list_entries()
    })


def entry(request, title):
    entry_content = utils.get_entry(title)
    if entry_content is None:
        raise Http404("Entry not found") #for raising a 404 error
    return render(request, "knowledge_base/entry.html", {
        "title": title,
        "content": entry_content
    })