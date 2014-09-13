from django.conf import settings
from django import template
settings.configure()

t=template.Template('''
{% for link in links %} {{forloop.counter}}-->{{link}} {% if not forloop.last%}|{% endif %}{% endfor %}''')
links=['LinkA','LinkB','LinkC','LinkD']
c =template.Context({'links':links})
print t.render(c)

'''
>>> 
 1-->LinkA | 2-->LinkB | 3-->LinkC | 4-->LinkD 
'''
