from functools import reduce
import math
import ttg


#####
def equiv(a:int, b:int, m:int) -> bool:
        """Checks if two integers are equivelent according to a specific modular"""
        a_rem = a % m
        b_rem = b % m
        return a_rem == b_rem



def truth_table(*argv) -> None:
        """
        Example: print(ttg.Truths(['p', 'q', 'r'], ['p and q and r', 'p or q or r', '(p or (~q)) => r']))
        
            negation: 'not', '-', '~'
            logical disjunction: 'or'
            logical nor: 'nor'
            exclusive disjunction: 'xor', '!='
            logical conjunction: 'and'
            logical NAND: 'nand'
            material implication: '=>', 'implies'
            logical biconditional: '='
        """
        print(ttg.Truths(*argv))

#####
def multiplicative_inverse(a: int, m: int) -> int:
    """
    Hvad skal vi gange a med, så modulos vores m giver 1.
    Given a and m, finds the number which times a gives modulos 1.
    Bemærk rækkefølgen.
    a skal være først, m skal følge efter. 
    """
    invers = 0
    while (invers*a) % m != 1:
        invers = invers + 1 
    return invers

#####
def relatively_prime(m:int,n:int) -> bool:
    """
    Checks if two numbers are relatively prime
    """
    return 1 == gcd(m,n)


#####
def pairwise_relatively_prime(v:list[int]) -> bool:
    """
    Checks if numbers in a list are pairwise relatively prime.
    >>> pairwise_relatively_prime([5,7,8])
    True
    """
    pairwise = True
    for e in possible_pairs(v):
        if gcd(e[0], e[1]) != 1:
            pairwise = False
    return pairwise

#####
def solve_congruense(a:int, equiv:int, m:int):
    """
    Solves a single congruense.
    First finds the inverse of a and m, and uses this to find the factor of
    the mod value necessary (the congruense) for mod m = 1.
    (Hvilken x værdi skal vi bruge, så mod m = 1).
    e.g 2x \equiv 7 = 17
    >>> solve_congruense(2,7,17)
    12
    """
    invers = multiplicative_inverse(a,m)
    print(f"Inversen er: {invers}")
    return (invers * equiv) % m

#####
def possible_pairs(v:list[int]) -> list[list]:
    """
    Returns a list with all possible (unordered) pairs from a list of numbers.
    >>> possible_pairs([1,2,3])
    [(1,2),(1,3),(2,3)]
    """
    pairs = []
    for i in range(len(v)):
        for j in range(1+i, len(v)):
            pairs.append((v[i],v[j]))
    return pairs

#####
def system_of_congruence(v:list[tuple]) -> int:
    """
    Takes a list with congruences, determines their common moduli and their least
    possible positive integer equivalence.

    IMPLEMENTER SÅLEDES DEN OGSÅ GIVER SKEMAET SOM OUTPUT?
    med kolonner for b, N, inverses, mods_products, products?
    
    >>> system_of_congruence([(1,3,5),(1,1,7),(1,6,8)])
    (78,'+', 280,'k')
    """

    b = [e[1] % e[2] for e in v] # remainders
    mods = [e[2] for e in v] # moduli
    mods_helper = [[x for x in mods if x != e] for e in mods] 
    N = [reduce(lambda a,b: a*b,x,1) for x in mods_helper] # products of modulis

    if pairwise_relatively_prime(mods):

        inverses = []
        i = 0
        while i < len(v):
            inverses.append(multiplicative_inverse(N[i], mods[i]))
            i = i + 1 

        products = []
        j = 0
        while j < len(v):
            products.append(b[j]*N[j]*inverses[j])
            j = j + 1

        mods_product = reduce(lambda x,y: x*y, mods, 1)

        answer = sum(products) % mods_product
    
        return answer,'+', mods_product, "k"

    else:
        return "The moduli of the equivalences are not pairwise relatively prime"

#####    
def is_prime(n: int) -> bool:
    """
    Checks whether n is a prime number.
    >>> is_prime(7)
    True
    """
    return 2 == reduce(lambda x, y: x+1 if n % y == 0 else x, range(1,n+1),0)

#####    
def gcd(m: int, n: int) -> int:
    """
    Computes the greatest common divisor of m and n using Euclides' algorithm.
    Usable to find if two numbers are relatively prime.
    
    >>> gcd(10,5)
    5
    """

    if m % n == 0: # er det ene tal allerede det højest mulige?
        return n
		
    else:
        m = m % n # ellers følges euklids algoritme (se under)
        return gcd(n, m)

    
####        
def eratothenes(n:int) -> list([int]):
    """
    Find all prime numbers up to n.
    Tanke: Går tallet op i det næste indtil n. Hvis ja, så er det ikke primtal.
    """
    up_to_n = [i for i in range(2,n+1)]
    for e in up_to_n:
        for j in up_to_n:
            if j % e == 0 and j != e:
                up_to_n.remove(j)

    return up_to_n


####
def lcm(a:int,b:int) -> int:
    """
    Returns the least common multiple.
    >>>lcm(3,4)
    12
    """
    return int((a * b) / gcd(a,b))  
    
####
def multGeneral(M:list[list[int]],N:list[list[int]]) -> list[list]:
    """
    Returns the result of multiplicating two matrices.
    Skal fikses til kun at tage imod to "mulige" matricer?
    """
    result = [[0 for x in range(len(N[0]))] for y in range(len(M))]

    for i in range(len(M)):
        for j in range(len(N[0])):
            for k in range(len(N)):
                result[i][j] = result[i][j] + M[i][k] * N[k][j]
                
    return result

####
def powerset(v: list) -> set:
    """
    Returns the powerset of a set.
    >>>powerset({1,2,3})
    {{1},{2},{3},{1,2},{2,1},{1,3},{3,1},{}}
    Konverter til mængde?
    """
    power_set = []
    x = len(v)
    for i in range(1 << x): ##bitewise operator
        power_set.append({v[j] for j in range(x) if (i & (1 << j))})
    return power_set

####
def generalized_pigeonhole(overflow:int,boxes:int) -> int:
    """
    Returns the number of objects necessary to return the given overflow.
    generalized_pigeonhole(3,2)
    5
    """
    _overflow = overflow - 1 
    n = (boxes * _overflow) + 1

    return n

#####
def permutations(n:int, r:int) -> int:
    """
    Returns the size of the r-permutation of the size of a set n.
    """
    res = 1
    i = 0
    while i < r:
        res = res * n
        i = i + 1
        n = n - 1
    return res

#####
def factorial(n:int) -> int:
    """
    Computes the factorial of a number.	
    >>>factorial(3)
    6
    """
    if n == 0:
        return 1
    else:
        return factorial(n-1)*n

#####
def combinations(n:int,r:int) -> int:
    """
    Returns the amount of combinations n chose r"
    """
    return int(permutations(n,r)/factorial(r))
#####
def matrice():
    """
    Creates a matrix based on user input.
    """

    size = input("Hvor stor skal matricen være? ")
    rows = int(size.split()[0])
    columns = int(size.split()[2])
    values = []
    for e in range(1,rows+1):
        values.append(input(f"Placer {columns} værdier i {e} række. "))

    matrice = [x.split(",") for x in values]

    print("Din matrice:")
    for e in matrice:
        print(e)

    print(values)
    return matrice
        

######
def prime_factorization(n: int) -> list[int]:
    """
    Returns the prime factors of n
    >>> prime_factorization(6)
    [2,3]
    """
    primes = eratothenes(n)
    factors = []
    for e in primes:
        if n % e == 0:
            factors.append(e)
    return factors 
        

    
######
def transpose(m: list[list]) -> list[list]:
    """
    Returns a matrix obtained from m by interchanging rows and columns.
    >>> transpose([[1,2,3],[4,5,6]])
    [[1,4],[2,5],[3,6]]
    """
    return [[x[e] for x in m] for e in range(len(m[0]))]


#######
def pascals_triangle(n:int) -> None:
    """
    Prints pascals triangle down to row n.
    >>> pascals_triangle(5)
    [1]
    [1,1]
    [1,2,1]
    [1,3,3,1]
    [1,4,6,4,1]
    [1,5,10,10,5,1]
    """
    i = 0
    for e in range(n+1):
        new_line=[]
        for j in range(i+1):
            new_line.append(combinations(e,j))
            
        i = i + 1
        
        print(new_line)

#### program der tjekker om to tal er kongruente?
#### progra mder tjekker om to tal er divisible?

