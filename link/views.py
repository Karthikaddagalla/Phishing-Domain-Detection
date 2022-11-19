from django.http import HttpResponse
from django.shortcuts import render
import sys

sys.path.append('../phishing_detection')

from CodeFiles.predictions import predictor

from link.forms import LinkInputForm


# Create your views here.

def testing(request):
    return HttpResponse("Testing the django")

def homepage(request):

    form = LinkInputForm
    values = {"form": form, "pred":"10"}

    if request.method == "POST":
        form = LinkInputForm(request.POST)

        if form.is_valid():
            given_link = form.cleaned_data["Enter_a_Valid_Link"]
            predict = predictor(given_link)
            values["link_is"] = given_link

            if predict == 0:
                values["pred"] = "0"
                return render(request, "index.html", values)
                

            elif predict == 1:
                values["pred"] = "1"
                return render(request, "index.html", values)


            elif predict == 5:
                values["pred"] = "5"
                return render(request, "index.html", values)

            else:
                values["pred"] = "2"   # The link is not working
                return render(request, "index.html", values)



    print(True)
    return render(request, "index.html", values)






