from logging import PlaceHolder, error

from django import forms
from django.http.response import HttpResponse
from django.shortcuts import render
from markdown2 import markdown

from .util import get_entry, list_entries, save_entry

class NewPageForm(forms.Form):
    #title field is normal text input
    title = forms.CharField(
        required=True,
        label= "",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Title",
                "class": "form-control w-50"
            }
            )
        )

    #content field is a large text box
    content = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Content",
                "class": "form-control w-75"
                })
        )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

#return a wiki entry passed as a parameter if it exists
def entry(request, entry):
    #get a list of all the current wiki pages available
    entries = [s for s in list_entries()]

    #check if wiki entry exists
    #canonicalise search string and list entries using .upper()
    if entry.upper() not in map(str.upper, entries):
        return render(request,"encyclopedia/error.html", {
            "message": "Wiki page for the chosen entry does not exist",
            "substrings": [s for s in entries if entry.upper() in s.upper()]    
        })  #additionally, search query might be a substring of any of the entries

    #render the remplate and pass in the markdown text
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": markdown(get_entry(entry))
    })    

#allow user to search for a wiki page
def search(request):
    #let entry() method handle the work
    query = request.POST["q"]
    return entry(request, query)

#TODO: create new entry
def new(request):
    #display page
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "form": NewPageForm()
        })
    else:   #else user submitted form via POST
        form = NewPageForm(request.POST)
        if form.is_valid():
            return HttpResponse(f"title = {form.cleaned_data['title']}, content = {form.cleaned_data['content']}")
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })

#TODO: edit current entries
def edit(request):
    return

#TODO: direct user to random wiki entry
def random(request):
    return
