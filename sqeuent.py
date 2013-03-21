import re


def getvars(expr):
    ''' Get distinct varibles from a expression '''    
    return list(set(re.findall(r'\w',expr)))


def checkand(expr):
    if expr.find('&')!= -1:
        tr = expr.partition('&')
        return [tr[0],tr[2]]
    return 0

def checkp(expr):
    if len(expr)==1 or len(expr[2:]) == 1:
        return expr
    return 0

def getop(expr):
    if expr.find('&')!=-1:
        return '&'
    if expr.find('->')!=-1:
        return '->'
    if expr.find('|')!=-1:
        return '|'
    
def main():
    seq = raw_input()
    match = re.search(r'(.*?)\|-(.*)',seq)
    if match :
        lhs = match.group(1)
        rhs = match.group(2)
        print 'LHS : ',lhs,", RHS : ",rhs
    else:
        print ' Missing " |- "'
    
    rvariables = getvars(rhs)
    print rvariables
    truths = []
    op = []
    premises = lhs.split(',')
    print premises
    for p in premises :
        res = checkp(p.strip())
        if res!=0:
            op.append(res)
            continue
        res = checkand(p.strip())
        if not (res == 0):
            for t in res :
                t = t.strip()
                if t not in truths:
                    truths.append(t)
        
    print truths
    for v in rvariables:
        if v not in truths:
            if v not in op:
                print 'The sequent is invalid'
                return 0
    count  = 1
    for p in premises:
        print count,'     ' , p , "\t premise"
        count+=1
    
    for t in truths:
        c = 0
        for p in premises:
            if p.find('&')!= -1:
                if p.find(t)!= -1:
                    c = p.index(t)+1
                  
        print count , '     ',t,'\t & elimination' ,'[',c,']'
        count+=1
    
    
    print count,'     ',rhs,'\t ',getop(rhs),'introduction'
        
        
    print 'Vars : ',rvariables
  

if __name__ == '__main__':
  main()       
