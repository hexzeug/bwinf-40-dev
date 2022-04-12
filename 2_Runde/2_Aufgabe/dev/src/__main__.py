import random
import argparse
from itertools import product as _product, chain as _chain
from statistics import median as _median

#int overloading hack for not allowing divison fraction results
class DivisionResultNotInteger(Exception): ...

class NoFractionInt(int):
    def __truediv__(self, __x: int) -> int:
        __r = super().__truediv__(__x)
        if __r.is_integer(): return int(__r)
        raise DivisionResultNotInteger()
    
    def __rtruediv__(self, __x: int) -> int:
        __r = super().__rtruediv__(__x)
        if __r.is_integer(): return int(__r)
        raise DivisionResultNotInteger()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"
    
    def __int__(self) -> int:
        return super().__int__()

OPERATIONS = ["+", "-", "*", "/"]

#parse arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("operation_count", type=int, help="count of the operations to guess in the output rizzle")
args = argparser.parse_args()
digits = args.operation_count + 1
if digits < 2:
    exit("The operation count must not be less than 1")

#generate numbers
numbers = [NoFractionInt(random.randint(1, 9)) for i in range(digits)]

#calculate results for substituting every possible operation combination between "numbers"
results = []
operation_lists = []
for operations in _product(OPERATIONS, repeat=digits - 1):
    operations = list(operations)
    expression = "".join(list(_chain(*list(zip([str(x) for x in numbers], operations))))) + str(numbers[-1])
    try: result = eval(expression)
    except DivisionResultNotInteger: continue
    if result <= 0: continue
    results.append(result)
    operation_lists.append(operations)

#remove duplicated solutions
for i, result in reversed(list(enumerate(results))):
    if results.count(result) > 1:
        results.pop(i)
        operation_lists.pop(i)

#remove too boring solutions
diversitys = [len(set(x)) for x in operation_lists]
solutions = list(zip(results, operation_lists, diversitys))
best_diversity = max(diversitys)
for i, solution in reversed(list(enumerate(solutions))):
    if solution[2] < best_diversity:
        solutions.pop(i)
del best_diversity

#sort list (after their distance of their result to the median of all results)
median = _median(results)
def solutionSorter(solution):
    return abs(median - solution[0])
solutions.sort(key=solutionSorter)
del median, solutionSorter

#output solution #TODO make better

output_solution = random.choices(solutions, weights=reversed(list(range(len(solutions)))))[0]

solution_str = f"{''.join(list(_chain(*list(zip([str(x) for x in numbers], output_solution[1])))))}{numbers[-1]}"
exec(f"calculated_result = int({solution_str})")

print(f"{'?'.join([str(int(x)) for x in numbers])}={output_solution[0]}")
print(f"{solution_str}={calculated_result}")