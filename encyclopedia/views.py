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
        return render(request, "encyclopedia/search.html", {
            "search_result": search_result
        })
                

