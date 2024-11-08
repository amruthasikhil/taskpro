def smap_dec(fn):
    
    def wrapper(n1,n2):
        
        if n1<n2:
            
            (n1,n2)=(n2,n1)
            
        return fn(n1,n2)
    return wrapper

@smap_dec
def smart_sub(n1,n2):
    
    return n1-n2

@smap_dec
def smart_div(n1,n2):
    return n1/n2


print(smart_sub(5,10))