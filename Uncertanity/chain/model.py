from pomegranate import *

#Define starting probabilities 
start = DiscreteDistribution({
    "sun": 0.5,
    "rain": 0.5
})

#Define transition model
transition = ConditionalProbabilityTable([
    ["sun", "sun", 0.8],
    ["sun", "rain", 0.2],
    ["rain", "sun", 0.3],
    ["rain", "rain", 0.7]
], [start])

#create Markov chain
model = MarkovChain([start, transition])

#sample 50 states from chain
print(model.sample(50)) 