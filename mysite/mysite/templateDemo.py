from django.conf import settings
from django import template

settings.configure()
t=template.Template("hello,{{name}}.")

for name in ('John','Julie','Pat'):
    print t.render(template.Context({'name':name}))

'''
>>> 
hello,John.
hello,Julie.
hello,Pat.
'''
