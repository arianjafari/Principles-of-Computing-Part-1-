"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    result = [0 for value in line]
        
    
    dummy_idx = 0    
    
    for idx, value in enumerate(line):
        if value != 0 :
            result[dummy_idx] = value
            dummy_idx += 1
            
    #new_result = [value for value in result]
    
    for idx in range(len(result)-1):
        
        if result[idx] == result[idx+1]:
            result[idx] = (2*result[idx])
            for dummy_idx in range(idx+1,len(result)-1):
                result[dummy_idx]=result[dummy_idx+1]
            result[len(result)-1] = 0    
 
        
    
    return result

#print(merge([4,0,2,2,2,2,2]))