from django.conf import settings
from django import template

settings.configure()
t=template.Template('''
{% for p in person_list  %} 
     <li>{{p.name}}></li>
     {% empty %}
     <p>NO Persosn.</p>
{% endfor %}''')
c =template.Context({'person_list': [{'name': 'personA_name'},
                                     {'name': 'personB_name'}]})
print t.render(c)
'''
>>> 
<li>personA_name></li> <li>personB_name></li>
'''

