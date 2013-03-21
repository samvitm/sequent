import re

''' Generate a truth table containig all possible values of the variable
    i.e 2**n numbers in binary, return a list of lists containg truth values
    of all variables in one row '''
def gentable(li):
    nos = len(li)
    table = []
    for x in range(pow(2,nos)):
        num = list(str(bin(x))[2:])
        z = nos - len(num)
        row = []
        for y in range(z):
            row.append('0')
        for d in num:
            row.append(d)
        table.append(row)
    for t in table:
        print t
    return table
       
'''Find right pair to the left braket'''
def frb(expr,i):
    rb = expr[:i].rfind('(')
    if rb!=-1:
        expr = expr[:rb]+'#'+expr[rb+1:]
        expr = expr[:i]+'!'+expr[i+1:]
        #print 'frb : : ' ,expr
        return expr

'''Find the open outermost bracket , returns its position'''    
def lob(expr):
    while(expr.count(')')!=0):
        cb = expr.find(')')
        expr = frb(expr,cb)
    return expr.rfind('(')

'''Removes 1 implication ( first from the left ) from an expression  '''
def implfree(expr):
    expr = '%' + expr + '%' 
    match = re.search(r'%(.*?)->(.*)%',expr)
    A = match.group(1)
    B = match.group(2)
    #print '1:  ',A,"     2 :  ",B
    rb = A.count('(')
    lb = A.count(')')
    
    if lb == rb:
        A = '~'+A
    else:
        b = lob(A)
        #b = A.rfind('(')
        A = A[:b+1]+ '~' + A[b+1:]
    B = '|'+B
    return A+B

''' Remove all implication from an expression '''
def rm_impl(expr):
    implications = expr.count('->')
    if implications:
        for x in range(implications):
            expr = implfree(expr)
    return expr

''' Get distinct varibles from a expression '''    
def getvars(expr):
    return list(set(re.findall(r'\w',expr)))

def main():
    seq = raw_input('Enter 2 formulae seperated by " = " \n ')
    match = re.search(r'(.*?)=(.*)',seq)
    if match :
        lhs = match.group(1)
        rhs = match.group(2)
        print 'LHS : ',lhs,", RHS : ",rhs
    else:
        print ' Missing " = "'

    lvariables = getvars(lhs)
    print lvariables
    truth_table = gentable(lvariables)
    f = 0
    lhs = rm_impl(lhs)
    rhs = rm_impl(rhs)
    print "LHS :: " , lhs
    print "RHS :: " , rhs
    results  = []
    for row in truth_table:
        eq1 = lhs
        eq2 = rhs
        for val,var in zip(row,lvariables):
            print var,"       ",val
            eq1 = eq1.replace(var,val)
            eq2 = eq2.replace(var,val)
        
        eq1 = eq1.replace('~',' not ')
        eq1 = eq1.replace('|',' or ')
        eq2 = eq2.replace('~',' not ')
        eq2 = eq2.replace('|',' or ')
        res_l = bool(eval(eq1))
        res_r = bool(eval(eq2))
        print 'Result :: lhs = ' , res_l ," , rhs = " ,res_r
        results.append([res_l,res_r])
        if bool(res_l)!=bool(res_r):
            f = 1
        print '\n'
    if f :
        print 'Not equivalent'
    else:
        print 'Equivalent'

    for r in results:
        print 'LHS:: ',r[0],'\tRHS::',r[1]

if __name__ == '__main__':
  main()       
