from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render

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
        return render(request,"encyclopedia/error.html")

    #render the remplate and pass in markdown text
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": markdown(get_entry(entry))
    })    