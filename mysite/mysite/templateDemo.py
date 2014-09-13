# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
settings.configure()

t=template.Template('''
{% for link in links %}
    {{ link}}
    {{ link|lower }}{# Upcase,Lowercase#}
    {{ link|first|upper }}
    {{ link|truncatewords:"3" }}
    {{ link|slice:"3" }}
{% endfor %}
''')
links=['linkA is a link .',u'我是中国人,我爱自己的祖国,你呢?是那国人?']
c =template.Context({'links':links})
print t.render(c)

