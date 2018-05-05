import itertools


framework = {}
descriptions = {}
arguments = set()
relations = set()
cfs = set()
grod = set()
prf = set()

def is_attacked(arg, relations):
    for x in relations:
        if x[1] == arg:
            return True

def attacks(x):
    return list(framework[x])

def get_arg_attackers(arg):
    attackers = []
    for i in relations:
        if i[1] == arg:
            attackers.append(i[0])
    return(set(attackers))

def get_attacked_args(set_of_args):

    attacked = set()
    for arg in set_of_args:
     for i in relations:
        if i[0] == arg:
         attacked.add(i[1])
    return (set(attacked))

#Pasted from Python Iter Recipes
def powerset(iterable):
    s = list(iterable)
    return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

def compute_cfs():

    pwr = powerset(arguments)
    for x in relations:
       x1 = x[0]
       x2 = x[1]
       todelete = []
       for i in pwr:
           if (x1 in i) and (x2 in i):
               todelete.append(i)
       for i in todelete:
           pwr.remove(i)
    cfs = pwr
    return cfs


    #return pwr

def compute_naive_extension(cfs):
    naive = []
    maxLen = 0

    for i in cfs:
        if len(i)>maxLen:
            maxLen = len(i)

    for i in cfs:
        if len(i)==maxLen:
            naive.append(i)

    return set(naive)


    # For each conflict free subset, if its attackers are
    # attacked (exhaustively) by a subset of that cfs, it is admissible

def compute_admissibility(cfs):

    admissible = []

    for cfset in cfs:
        attackers = set()

        for cfsetmember in cfset:
            attackers = attackers.union(get_arg_attackers(cfsetmember))

        attackedbycfsmembers = []

        for attacker in attackers:
            atk = False
            attackedby = get_arg_attackers(attacker)


            for cfsetmember in cfset:
                if cfsetmember in attackedby:
                    atk = True
            attackedbycfsmembers.append(atk)

        if all(attackedbycfsmembers):
            admissible.append(cfset)


    return set(admissible)

def compute_stable_extension(adm):

    stb = []

    for x in adm:
         if set(x).union(get_attacked_args(x)) == arguments:
            stb.append(x)
    return set(stb)

def compute_grounded_extension(adm):

    grd = []
    rel = list(relations)
    attackedbyin = []
    someArg = True

    if len(adm)== 1:
        return grd


    for x in arguments:
            if is_attacked(x, rel) != True:
                if x not in grd:
                    grd.append(x)

    if len(grd)==0:
        return grd

    while someArg:
        for x in grd:
            if len(framework[x]) <= 1:
                attackedbyin.append(*framework[x])
            else :
                attackedbyin.extend(framework[x])

        for r in rel:
            for atk in attackedbyin:
                if r[0]== atk:
                    rel.remove(r)

        for i in arguments:
            if is_attacked(i, rel) != True:
                if i not in grd:
                    grd.append(i)
                else:
                    someArg = False


    return grd

def compute_preferred_extensions(adm):

    pref = []
    maxLen = 0

    for i in adm:
        if len(i)>maxLen:
            maxLen = len(i)

    for i in adm:
        if len(i)==maxLen:
            pref.append(i)

    return set(pref)

def compute_complete_extensions(adm):



    grd = set(compute_grounded_extension(adm))
    prf = compute_preferred_extensions(adm)

    grd2 = str(grd).replace("'",'')
    prf2 = str(prf).replace('(','').replace(',','').replace(')','').replace("'",'')


    if prf2 == grd2:
        return prf2
    else:
        return grd2+" "+prf2











