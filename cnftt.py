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

'''Generates a disjuction'''
def gendis(row,variables):
    expr = ''
    c  = 0
    for value in row[:-1]:
        #print value
        if value == '0':
            expr+='~'+variables[c]
        else:
            expr+=variables[c]
        expr+='|'
        c+=1
    #print "EXPR :: ",expr
    return '('+expr[:-1]+')'

'''Takes a truth table ofthe formula and return its CNF'''
def cnf(table,var):
    ftable = []
    expr = ''
    for row in table:
        if row[-1] == False:
            ftable.append(row)
    #print 'False rows :: '
    for t in ftable: expr+= gendis(t,var)+'&'        
    return expr[:-1]
        

def main():
    expr = raw_input('Enter a logical formula : ')
    variables = getvars(expr)
    #print variables
    truth_table = gentable(variables)
    f = 0
    expr = rm_impl(expr)
    print "\n\nImplication Free :: " , expr
    results  = []
    for row in truth_table:
        eq = expr
        for val,var in zip(row,variables):
            #print var,"       ",val
            eq = eq.replace(var,val)
        eq = eq.replace('~',' not ')
        eq = eq.replace('|',' or ')
        result = eval(eq)
        #print 'Result :: = ' , result
        row.append(bool(result))

    print '\nTruth Table'
    print '-----------------------------------------'
    print variables,'Result'
    for t in truth_table:  print t       
    print'\nCNF'
    print '--------------------------------'
    print cnf(truth_table,variables)   

if __name__ == '__main__':
  main()       
