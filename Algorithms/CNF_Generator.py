import random

def generate_clause(num_vars):
    clause_length = random.randint(1, min(5, num_vars))  # avoid overly large clauses
    clause = set()
    while len(clause) < clause_length:
        var = random.randint(1, num_vars)
        lit = var if random.choice([True, False]) else -var
        clause.add(lit)
    return list(clause)

def generate_cnf_problem(num_vars, num_clauses):
    clauses = [generate_clause(num_vars) for _ in range(num_clauses)]
    return clauses

def write_dimacs(filename, problems, num_vars_list):
    with open(filename, "w") as f:
        for i, (clauses, num_vars) in enumerate(zip(problems, num_vars_list), 1):
            f.write(f"c Problem {i}\n")
            f.write(f"p cnf {num_vars} {len(clauses)}\n")
            for clause in clauses:
                f.write(" ".join(str(lit) for lit in clause) + " 0\n")
            f.write("\n")  # Separate problems

def main():
    filename = "generated_problem.cnf"
    problems = []
    num_vars_list = []

    print("Generating CNF problem...")
    
    num_vars = int(input(f"Enter number of variables for problem : "))
    num_clauses = int(input(f"Enter number of clauses for problem : "))
    problem = generate_cnf_problem(num_vars, num_clauses)
    problems.append(problem)
    num_vars_list.append(num_vars)

    write_dimacs(filename, problems, num_vars_list)
    print(f"\nDone! CNF file with 10 problems saved as '{filename}'")

if __name__ == "__main__":
    main()
