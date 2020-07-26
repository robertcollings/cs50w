from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
import markdown2
from django.urls import reverse
from django.shortcuts import redirect
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, name):
    
    if name in util.list_entries():
        content = markdown2.markdown(util.get_entry(name))

        return render(request, "encyclopedia/page.html", {
            "content": content, "title": name
        })

    else:
        return HttpResponseNotFound("Error 404: page does not exist")

def search(request):
    # If arriving from a search query:
    if request.method == "POST":

        # Get the search query
        query = request.POST.get("q") 
        
        # Check if the query is in the list
        if query in util.list_entries():

            # Retrieve the page if yes
            print("here")
            return redirect(reverse('encyclopedia:page', kwargs={'name':query}))

        else:
            # Initiate a list of similar pages
            results = []

            # Loop over similar pages and add to list
            for page in util.list_entries():
                if query in page.lower():
                    results.append(page)

            # Return the search page with list of similar pages
            return render(request, "encyclopedia/search.html", {
                "results":results
            })
    # If search page is URL'd directly then return empty search page
    return render(request, "encyclopedia/search.html")
    
def new_page(request):

    # If arriving from a form submission:
    if request.method == "POST":

        # Get the title and content
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        # Check page is not a duplicate
        if title in util.list_entries():
            return HttpResponseNotFound("Page already exists")

        # Save page to disk
        util.save_entry(title, content)

        # Convert markdown to HTML
        content = markdown2.markdown(content)

        return render(request, "encyclopedia/page.html", {
            "content": content, "title": title
        })

    return render(request, "encyclopedia/new-page.html")

def edit_page(request, name):
    
    if request.method == "POST":
        # Get the title and content
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Overrite page
        util.save_entry(name, content)

        # Convert markdown to HTML
        content = markdown2.markdown(content)

        # Return the new page
        return render(request, "encyclopedia/page.html", {
            "content": content, "title": title
        })

    # Get content
    content = util.get_entry(name)

    return render(request, "encyclopedia/edit-page.html", {
            "content": content, "title": name
        })

def delete(request, name):

    if request.method == "POST":

        # Get the title
        title = request.POST.get("title")
        
        util.delete_entry(title)

        return redirect(reverse('encyclopedia:index'))


def randompg(request):
    number = random.randrange(0,len(util.list_entries()))
    pages = util.list_entries()

    return redirect(reverse('encyclopedia:page', kwargs={'name':pages[number]}))