import re

match_dog = re.match(r'dog','dog cat dog')
print match_dog.group(0)
print match_dog.start()
print match_dog.end()

search_cat = re.search(r'cat', 'dog cat dog')
print search_cat.group(0)

findall_dog = re.findall(r'dog','dog cat dog')
print findall_dog

findall_cat = re.findall(r'cat','dog cat dog')
print findall_cat


contactInfo = 'Doe,John:555-1212'
search_contact = re.search(r'(\w+),(\w+):(\S+)', contactInfo)
print search_contact.group(0)
print search_contact.group(1)
print search_contact.group(2)
print search_contact.group(3)

search_contact_by_name = re.search(
    r'(?P<last>\w+),(?P<first>\w+):(?P<phone>\S+)',
    contactInfo)
print search_contact_by_name.group('last')
print search_contact_by_name.group('first')
print search_contact_by_name.group('phone')

'''
dog
0
3
cat
['dog', 'dog']
['cat']
Doe,John:555-1212
Doe
John
555-1212
Doe
John
555-1212
'''

