from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown

from .util import get_entry, list_entries, save_entry


#django form
class EntryForm(forms.Form):
    #title field is normal text input
    title = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Title",
                "class": "form-control w-50"
            }
            )
        )

    #content field is a large text box
    markdown = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Markdown content",
                "class": "form-control w-75"
                })
        )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

#return a wiki entry passed as a parameter if it exists
def entry(request, entry):
    #check if wiki entry exists
    #canonicalise search string and list entries using .upper()
    if entry.upper() not in map(str.upper, list_entries()):
        return render(request,"encyclopedia/error.html", {
            "message": "Wiki page for the chosen entry does not exist",
            "substrings": [s for s in list_entries() if entry.upper() in s.upper()]    
        })  
        #additionally, search query might be a substring of any of the entries (this is checked in template via Jinja)

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

#allow user to create new entry
def new(request):
    #display page
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "form": EntryForm()
        })
    #else user submitted form via POST
    else:   
        #get POST data
        form = EntryForm(request.POST)

        #if form is invalid, re-render the page with existing info
        if not form.is_valid():
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
        
        #extract title and markdown content
        title = form.cleaned_data['title']
        markdown = form.cleaned_data['markdown']

        #check if wiki entry already exists, if it does, return an error message
        if title.upper() in map(str.upper, list_entries()):
            return render(request, "encyclopedia/error.html", {
                "message": "Wiki entry for this topic already exists"
            })
        
        #save the wiki entry and redirect user to index
        save_entry(title, markdown)
        return HttpResponseRedirect(reverse("index"))

#allow user to edit a chosen wiki page
def edit(request, entry):
    #GET request: display editing page
    if request.method == "GET":
        #retreive markdown content for the entry chosen to edit 
        form = EntryForm(initial={
            "title": entry,
            "markdown": get_entry(entry)
            }
        )

        #pass markdown content into template
        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "form": form
        }) 
    #else, user submitted form via POST
    else:
        #validate form pubmission 
        form = EntryForm(request.POST)
        if not form.is_valid():
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
        
        #retreive form fields
        title = form.cleaned_data["title"]
        markdown = form.cleaned_data["markdown"]

        #check if user inspected element and tried to "hack"
        if title.upper() not in map(str.upper, list_entries()):
            return render(request, "encyclopedia/error.html", {
                "message": "The wiki page you have chosen to edit does not exist. Hmm... Did you inspect element and try to 'hack' this page? :)"
            })

        #save entry and redirect user to the wiki page of the entry they edited
        save_entry(title, markdown)
        return HttpResponseRedirect(reverse("entry", args=[title]))

#TODO: direct user to random wiki entry
def random(request):
    return
