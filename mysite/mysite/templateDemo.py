from django.conf import settings
from django import template

settings.configure()
t=template.Template("{% for p in person_list reversed %} <li>{{p}}></li>{% endfor %}")
name_list=['AAA','BBB','CCC']
print t.render(template.Context({'person_list':name_list}))

'''
>>> 
li>CCC></li> <li>BBB></li> <li>AAA></li>
'''

