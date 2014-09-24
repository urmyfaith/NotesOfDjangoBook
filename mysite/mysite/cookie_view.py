from django.shortcuts import render_to_response
from django.http import HttpResponse

def show_color(request):
    if "favorite_color" in request.COOKIES:
        return HttpResponse("Your favourite color is %s" % \
                            request.COOKIES["favorite_color"])
    else:
        return HttpResponse("You don't have a favorite color.")
def set_color(request):
    if "favourite_color" in request.GET:
        response = HttpResonse("Your favourite color is now %s" % \
                              request.GET["favourite_color"]
                              )
        response.set_cookie("favourtie_color",request.GET["favourite_color"])
        return response
    else:
        return HttpResponse("You don't have a favorite color.")
