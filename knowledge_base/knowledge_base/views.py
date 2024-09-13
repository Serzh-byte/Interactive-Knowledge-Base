from django.shortcuts import render, redirect, Http404
from django import forms
from django.contrib import messages  # Import messages for notifications
import random
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

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Content")

def edit_page(request, title):
    # Get the current entry content
    entry = utils.get_entry(title)

    if entry is None:
        raise Http404("Entry not found")

    # If the form was submitted, process the changes
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            # Get the updated content from the form
            updated_content = form.cleaned_data["content"]
            # Save the updated content
            utils.save_entry(title, updated_content)
            # Redirect to the updated entry's page
            return redirect('entry', title=title)

    # For a GET request, pre-populate the form with the existing content
    form = EditPageForm(initial={"content": entry})

    return render(request, "knowledge_base/edit_page.html", {
        "form": form,
        "title": title
    })

def search(request):
    query = request.GET.get("q", "").strip().lower()
    if not query:
        return render(request, "knowledge_base/search_results.html", {
            "query": query,
            "results": []
        })

    entries = utils.list_entries()
    
    # Exact match
    if query in [entry.lower() for entry in entries]:
        return redirect("entry", title=next(entry for entry in entries if entry.lower() == query))
    
    # Partial match
    results = [entry for entry in entries if query in entry.lower()]
    
    # If no partial matches, try fuzzy matching
    if not results:
        from difflib import get_close_matches
        results = get_close_matches(query, entries, n=5, cutoff=0.6)

    return render(request, "knowledge_base/search_results.html", {
        "query": query,
        "results": results
    })

def random_page(request):
    # Get all the available entries
    entries = utils.list_entries()   
    
    # Pick a random entry
    random_entry = random.choice(entries)
    
    # Redirect to the selected random entry's page
    return redirect('entry', title=random_entry)

def delete_page(request, title):
    # Check if the entry exists
    if utils.get_entry(title):
        # Delete the entry
        utils.delete_entry(title)
        # Add a success message
        messages.success(request, f'Entry "{title}" has been deleted.')
        # Redirect to the index page
        return redirect('index')
    else:
        # Add an error message
        messages.error(request, 'Entry not found.')
        return redirect('index')