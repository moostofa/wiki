from logging import error
from django.http.response import HttpResponse
from django.shortcuts import render
from django import forms

from markdown2 import markdown

from .util import list_entries, save_entry, get_entry

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

def entry(request, entry):
    #return the wiki entry passed as parameter if it exists

    #check if wiki entry exists
    entries = [element.upper() for element in list_entries()]
    if entry.upper() not in entries:
        return render(request,"encyclopedia/error.html", {
            "message": "Wiki page for the chosen entry does not exist"
        })

    #render the remplate and pass in the markdown text
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": markdown(get_entry(entry))
    })    

#TODO: search entry
def search(request):
    if request.method == "POST":
        q = request.POST["q"]
        return entry(request, q)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Something went wrong, search form should not have method of GET"
        })

def new(request):
    #TODO: create new entry
    return

def edit(request):
    #TODO: edit current entries
    return

def random(request):
    #TODO: direct user to random wiki entry
    return