from model import model

# Calculate probability for a given observation
probability = model.probability([["none","no","ontime","attend"]])

print(probability)