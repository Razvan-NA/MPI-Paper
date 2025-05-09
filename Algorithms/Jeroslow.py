import time
import tracemalloc
from pysat.formula import CNF
from collections import defaultdict

MAX_STEPS = 1_000_000
TIME_LIMIT = 10  # Set your time limit in seconds

def jeroslow_wang(clauses, assignment):
    scores = defaultdict(float)
    for clause in clauses:
        if any(lit in assignment for lit in clause):  # Clause already satisfied
            continue
        for lit in clause:
            if lit not in assignment and -lit not in assignment:
                scores[lit] += 2 ** (-len(clause))
    return max(scores, key=scores.get, default=None)

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            unassigned = [lit for lit in clause if lit not in assignment and -lit not in assignment]
            if len(unassigned) == 1:
                unit = unassigned[0]
                assignment.add(unit)
                changed = True
                break
            elif all(-lit in assignment for lit in clause):
                return False  # Conflict
    return True

def dpll(clauses, assignment=set(), steps=[0], start_time=None):
    # Check if time limit is exceeded
    if time.time() - start_time > TIME_LIMIT:
        return None  # Timeout

    if steps[0] >= MAX_STEPS:
        return None

    steps[0] += 1
    if not unit_propagate(clauses, assignment):
        return False

    if all(any(lit in assignment for lit in clause) for clause in clauses):
        return True

    literal = jeroslow_wang(clauses, assignment)
    if literal is None:
        return True  # All clauses satisfied

    for val in [literal, -literal]:
        new_assignment = assignment.copy()
        new_assignment.add(val)
        result = dpll(clauses, new_assignment, steps, start_time)
        if result is True:
            return True
        if result is None:
            return None
    return False

def main():
    filename = "CBS_k3_n100_m403_b10_2.cnf"  # Change this to your CNF file name
    cnf = CNF(from_file=filename)
    clauses = [list(clause) for clause in cnf.clauses]

    tracemalloc.start()
    start_time = time.time()

    result = dpll(clauses, start_time=start_time)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"File: {filename}")
    if result is True:
        print("Result: SAT")
    elif result is False:
        print("Result: UNSAT")
    else:
        print("Result: UNKNOWN (time limit or step limit reached)")
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    print(f"Peak Memory Usage: {peak / 1024:.2f} KB")

if __name__ == "__main__":
    main()
