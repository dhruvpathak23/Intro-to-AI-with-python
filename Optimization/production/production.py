import scipy.optimize

# Objective Function: 50x_1 + 80x_2
# constraint 1: 5x_1 + 2x_2 <= 20
# constraint 2: -10x_1 + -12x_2 <= -90

result = scipy.optimize.linprog(
    [50,80], # Cost function: 50x_1 + 80x_2
    A_ub=[[5, 2], [-10, -12]], # Coefficients for the inequality constraints
    b_ub=[20, -90], # Constants for the inequalities: 20 and  -90 
)

if result.success:
    print(f"X1: {round(result.x[0], 2)} hours")
    print(f"X2: {round(result.x[1], 2)} hours")
else:
    print("No Solution")    