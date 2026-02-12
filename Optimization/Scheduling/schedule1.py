from constraint import *

problem = Problem()

# Add Variables
problem.addVariables(
    ["a","B","C","D","E","F","G"],
    ["Monday","Tuesday","Wednesday"]
)
 
# Add Constraints
CONSTRAINTS = [
     ("A", "B"), 
    ("A", "C"), 
    ("B", "D"),
    ("B", "C"), 
    ("B", "E"),
    ("C", "E"), 
    ("C", "F"),
    ("D", "E"), 
    ("E", "F"), 
    ("E", "G"),
    ("F", "G")
]
for x,y in CONSTRAINTS:
    problem.addConstraint(lambda x,y: x != y, (x,y))

# Solve problem
for solution in problem.getSolutions():
    print(solution)    