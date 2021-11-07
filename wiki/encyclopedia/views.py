from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from . import util
from django import forms
from markdown2 import markdown
import random

class nt (forms.Form):
    entry = forms.CharField(label= '' ,
    widget=forms.TextInput(attrs={'placeholder': 'Search encyclopedia'}))

class npt (forms.Form):
    title = forms.CharField(label='Title')
    
class npd (forms.Form):
    dis = forms.CharField(label="Discription" ,
    widget=forms.Textarea(attrs= {'rows': 1, 'cols': 40, 
    'style' : 'height : 100px'}),
     
    )




    


def index(request):
    

    if request.method == "POST":
        qq = nt(request.POST)
        
        if qq.is_valid():
        
            q = qq.cleaned_data["entry"]
            x = util.get_entry(q)
            if x != None:

                 return HttpResponseRedirect(reverse("search" , args= [q]))
            else :
                 return HttpResponseRedirect(reverse("results", args=[q]))
                 
                 
        else:
            return render(request, "encyclopedia\index.html",{
                "search" : qq, "entries": util.list_entries()
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "search" : nt()
    })
    
def search (request, q):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("edit", args=[q]))
                      
    try:
         edit = "<form method=\"POST\">"
         tkn = "{% csrf_token %}"
         editt= "<input type=\"submit\" value=\"Edit\">"
         edittt = "</form>"
         entry = util.get_entry(q)
         entryy = markdown(entry)
         path = f"D:\\Ahmed\\MF\\wiki\\encyclopedia\\templates\\encyclopedia\\{q}.html"
         with open(path, 'w',) as w:
             w.write(entryy)
             w.write(f"<title> {q.upper()} </title> \n")
             w.write("<br>\n")
             w.write(edit)
             w.write(tkn)
             w.write(editt)
             w.write(edittt)
         return render(request, f"encyclopedia/{q}.html")
    
    except TypeError:
        return render (request, "encyclopedia/nf.html")
    

def results (request, q):
    util.results(q)
   
    return render (request, "encyclopedia\sresults.html",{
                     "results" : util.resultss, "q" : q
                 })
    
def npage (request):
    
   
    listt = util.list_entries()
    if request.method == "POST":
        nppd = npd(request.POST)
        nppt = npt(request.POST)

        if nppd.is_valid() and nppt.is_valid():
             title = nppt.cleaned_data["title"]          
             dis = f"# {title.capitalize()}"
             dis += "\n"
             dis += "\n"
             dis += nppd.cleaned_data["dis"] 
             
             
             if title in listt or title.upper() in listt or title.capitalize() in listt or title.lower() in listt :
                 return HttpResponse (f"Error: Sorry this page already exists.")
             else :
                util.save_entry(title, dis)
                entry = util.get_entry(title)
                entryy = markdown(entry)
                path = f"D:\\Ahmed\\MF\\wiki\\encyclopedia\\templates\\encyclopedia\\{title}.html"
                with open(path, 'w',) as w:
                    w.write(entryy)
                    w.write(f"<title> {title.upper()} </title>")
                return render(request, f"encyclopedia/{title}.html")         


    return render (request, "encyclopedia\\newpage.html",{
        "title" : npt(), "dis" : npd()
    })

def rpage (request):
    entries = util.list_entries()
    
    q = random.choice(entries)
    return HttpResponseRedirect(reverse("search" , args= [q]))


def edit (request, q):

    entry = util.get_entry(q)
    class edita (forms.Form):
        md = forms.CharField(label="The  Markdown content of the page " ,
        widget=forms.Textarea(attrs= {'rows': 1, 'cols': 40, 
        'style' : 'height : 100px'}), initial= entry.strip()
    )
    
    if request.method == "GET":
         ediit = "<form method=\"POST\">"
         tkn = "{% csrf_token %}"
         editt= "<input type=\"submit\" value=\"Save Changes\">"
         edittt = "</form>"
         path = f"D:\\Ahmed\\MF\\wiki\\encyclopedia\\templates\\encyclopedia\\edit{q}.html"
         with open(path, 'w',) as w:
            w.write(f"<title> {q.upper()}(edit) </title> \n")
            w.write(f"<h1> {q} </h1>\n")
            w.write("<br> <br> \n")
            
            w.write(ediit)
            w.write("{{ form }} \n")
            w.write(tkn)
            w.write(editt)
            w.write(edittt)


         return render (request, f"encyclopedia\\edit{q}.html",{
            "form" : edita(), "q" : q
         })

    elif request.method == "POST":
         content = edita (request.POST)
         
         if content.is_valid():
             qq = content.cleaned_data["md"]
             util.save_entry(q, qq)
             return HttpResponseRedirect(reverse("search" , args= [q])) 
 


    