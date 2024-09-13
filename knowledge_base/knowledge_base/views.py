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
        raise Http404("Entry not found")
    return render(request, "knowledge_base/entry.html", {
        "title": title,
        "content": entry_content
    })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title", widget=forms.TextInput(attrs={'class': 'form-control'})) 
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Content")

def add_book(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if entry already exists
            if utils.get_entry(title):
                return render(request, "knowledge_base/add_book.html", {
                    "form": form,
                    "error": "An entry with this title already exists."
                })
            else:
                utils.save_entry(title, content)
                return redirect('entry', title=title)

    else:
        form = NewPageForm()

    return render(request, "knowledge_base/add_book.html", {"form": form})
