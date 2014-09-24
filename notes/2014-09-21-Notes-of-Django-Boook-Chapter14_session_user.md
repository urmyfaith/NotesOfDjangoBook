# Chapter 14 session_user



##存、取cookie

取出cookie:
> request.COOKIES["favorite_color"]

```python
# mysite/cookie_view.py
def show_color(request):
    if "favorite_color" in request.COOKIES:
        return HttpResponse("Your favourite color is %s" % \
                            request.COOKIES["favorite_color"])
    else:
        return HttpResponse("You don't have a favorite color.")
```

存cookie:
>  response.set_cookie("favourtie_color",cookie_value)

```python
# mysite/cookie_view.py
def set_color(request):
    if "favourite_color" in request.GET:
        response = HttpResonse("Your favourite color is now %s" % \
                              request.GET["favourite_color"]
                              )
        response.set_cookie("favourtie_color",request.GET["favourite_color"])
        return response
    else:
        return HttpResponse("You don't have a favorite color.")
```

![cookie_view.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/cookie_view.png)

----



