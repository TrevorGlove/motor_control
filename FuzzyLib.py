def Rules(rules, *args):
    for rule in rules:
        if rule[:-1] == args:
            return rule[-1]
    raise NameError("No rule found matching the supplied values") 

def Trapmf(x, membresia):
    if len(membresia) != 4:
        raise ValueError("membresia should have exactly 4 values")
    
    a, b, c, d = membresia
    
    if a <= x < b:
        return round((x - a) / (b - a), 3)
    elif b <= x <= c:
        return 1.0
    elif c < x <= d:
        return round((d - x) / (d - c), 3)
    else:
        return 0.0

def Trimf(x, membresia):
    if len(membresia) != 3:
        raise ValueError("membresia should have exactly 3 values")
    
    a, b, c = membresia
    if x < a or x > c:
        return 0.0
    elif a <= x < b:
        return round((x - a) / (b - a), 3)
    elif b <= x <= c:
        return round((c - x) / (c - b), 3)
    else:
        return 1.0

def Values(x, memberships):
    values = {m: (Trimf(x, m) if len(m) == 3 else Trapmf(x, m)) for m in memberships}
    if any(len(m) not in (3, 4) for m in memberships):
        raise ValueError("Memberships must have 3 or 4 values")
    return values

def Combination_membership(rules, values):
    results = []

    def generate_combinations(universes, current_combination):
        if not universes:
            result = Rules(rules, *current_combination)
            results.append(result)
        else:
            universe = universes[0]
            for value in universe:
                generate_combinations(universes[1:], current_combination + (value,))
    
    generate_combinations(values, ())
    return results

def Combination_values(values):
    min_values = []

    def combine_lists(values, current_combination, index):
        if index == len(values):
            min_value = min(current_combination)
            min_values.append(min_value)
        else:
            for item in values[index]:
                combine_lists(values, current_combination + [item], index + 1)

    combine_lists(values, [], 0)
    return min_values

def Fuzzy(R, inputs, universes):
    if len(inputs) != len(universes):
        raise ValueError("The number of entries must be equal to the number of universes")
    
    claves = []  
    values = []
    
    for x, universe in zip(inputs, universes):
        result = Values(x, universe)
        claves.append(list(result.keys()))
        values.append(list(result.values()))
       
    membership_out = Combination_membership(R, claves)
    values_out = Combination_values(values)
    
    grouped_values = {}
    for membership, value in zip(membership_out, values_out):
        grouped_values.setdefault(membership, []).append(value)
    
    max_values = {membership: max(values) for membership, values in grouped_values.items()}
    
    return max_values


def Inverse_trapmf(y, membresias):
    if y < 0.0 or y > 1.0:
        return None
    elif 0.0 <= y <= 1.0:
        a, b, c, d = membresias
        
        if y == 0.0:
            return a, d  
        elif y == 1.0:
            return b, c  
        elif 0 < y < 1 and a != b and c != d:
            x1 = a + (b - a)*y
            x2 = d - (d - c)*y
            return x1, x2
        elif 0 < y < 1 and a == b and c != d:
            x1 = a
            x2 = d - (d - c)*y
            return x1, x2
        elif 0 < y < 1 and a != b and c == d:
            x1 = a + (b - a)*y
            x2 = d
            return x1, x2
        elif 0 < y < 1 and a == b and c == d:
            return a, d
        elif 0 < y < 1 and b == c:
            x1 = a + (b - a)*y
            x2 = d - (d - c)*y
            return a, d
        else:
            return None
    else:
        return None
         
            
def Inverse_trimf(y, membresias):
    if y < 0.0 or y > 1.0:
        return None  
    
    a, b, c = membresias
    x1 = a + (b - a) * y
    x2 = c - (c - b) * y
    
    return x1, x2

def Proyect(val_fuzzyfic):
    zm = {}
    
    for membership, value in val_fuzzyfic.items():
        if len(membership) == 3:
            projection = Inverse_trimf(value, membership)
        elif len(membership) == 4:
            projection = Inverse_trapmf(value, membership)
        zm[membership] = projection
    
    return zm

def Cut(lines, values_F):
    updated_out = {}

    for membership, values in lines.items():
        if len(membership) == 3:
            updated_out[membership] = [membership[0], values[0], values[1], membership[2], values_F[membership]]
        elif len(membership) == 4:
            updated_out[membership] = [membership[0], values[0], values[1], membership[3], values_F[membership]]

    return updated_out

def Trapzmf(x, membresia):
    a, b, c, d, h = membresia  
    if len(membresia) != 5:  
        raise ValueError("membresia should have exactly 5 values")
    if x < a or x > d:
        return 0.000
    elif a <= x < b:
        return round((x - a) / (b - a) * h, 3)  
    elif b <= x < c:
        return h
    elif c <= x < d:
        return round((d - x) / (d - c) * h, 3)  
    elif c == d and x == d:
        return h
    elif a == b and x == a:
        return h
    elif b == c and x == b:
        return h 
    else:
        return 0.000

def Defuzzy(membership_out, universe, n):
    num_functions = len(membership_out)
    
    sumy = 0.0
    sumy_x = 0.0
    
    delta_x = (universe[1] - universe[0]) / n 
    
    for i in range(n):
        x = universe[0] + i * delta_x 
        
        max_value = 0.0
        
        for membresia in membership_out.values():
            mf_value = Trapzmf(x, membresia)
            max_value = max(max_value, mf_value)
        
        sumy += max_value
        sumy_x += max_value * x
    
    if sumy == 0:
        return 0.0  
    else:
        return sumy_x / sumy