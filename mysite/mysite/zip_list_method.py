x=[1,2,3]
print "type(x)=",type(x)    #type(x)= <type 'list'>
y=[4,5,6]

zipped=zip(x,y)
print "zippped=",zipped     #zippped= [(1, 4), (2, 5), (3, 6)]
print "type(zipped)=",type(zipped)  #type(zipped)= <type 'list'>

x2,y2=zip(*zipped)
print "x2=",x2,"\ty2=",     #x2= (1, 2, 3) 	y2= (4, 5, 6)
print "type(x2)=",type(x2)  #type(x2)= <type 'tuple'>

x2_list=list(x2)
print "x2_list=",x2_list    #x2_list= [1, 2, 3]
print "type(x2_list)=",type(x2_list)    #type(x2_list)= <type 'list'>

