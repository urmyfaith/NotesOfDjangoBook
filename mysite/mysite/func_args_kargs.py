# func_args_kargs

'''
func-->function
args-->arguments
kwargs-->keyword_arguments
'''
def foo(say_hello,age='20',*args,**kwargs):
    print "say_hello=",say_hello
    print "age=",str(age)
    print "Postional arguments arg:"
    print args
    print "Keyword arguments are:"
    print kwargs

print foo(1,2,3)

print foo('world',1, 2, name='Adrian', framework='Django')

print foo(40,4,name='zx', framework='web.py')

'''
>>>
say_hello= 1
age= 2
Postional arguments arg:
(3,)
Keyword arguments are:
{}
None

say_hello= world
age= 1
Postional arguments arg:
(2,)
Keyword arguments are:
{'framework': 'Django', 'name': 'Adrian'}
None

say_hello= 40
age= 4
Postional arguments arg:
()
Keyword arguments are:
{'framework': 'web.py', 'name': 'zx'}
None
'''
