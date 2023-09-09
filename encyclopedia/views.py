from django.shortcuts import render
import markdown

from . import util

def md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = md_to_html(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    

def search(request):
    if request.method == "POST":
        title_search =request.POST['q']
        content = md_to_html(title_search)
        if content:
            return render(request, "encyclopedia/entry.html", {
            "title": title_search,
            "content": content
        })
        entries = util.list_entries()
        search_result = []
        for entry in entries:
            if title_search.lower() in entry.lower():
                search_result.append(entry)

        if len(search_result) > 0:
            return render(request, "encyclopedia/search.html", {
            "search_result": search_result
            })
        else:
            return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content'] 
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": "Title and content already exists"
            })
        else:
            util.save_entry(title, content)
            new_content = md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": new_content
            })
                
def edit(request):
    if request.method == "POST":
        title = request.POST['title_entry']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content) 
        new_content = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": new_content
        })
