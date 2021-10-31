from logging import error

from django import forms
from django.http.response import HttpResponse
from django.shortcuts import render
from markdown2 import markdown

from .util import get_entry, list_entries, save_entry


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
    return render(request, "encyclopedia/new.html")

#TODO: edit current entries
def edit(request):
    return

#TODO: direct user to random wiki entry
def random(request):
    return
