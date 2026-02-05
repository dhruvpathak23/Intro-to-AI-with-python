from logic import *

rain = Symbol("rain") # It is raining.
hagrid = Symbol("hagrid") # Harry visited Hagrid.
dumbledore = Symbol("dumbledore") # Harry visited Dumbledore.

#sentence = And(rain, hagrid)
#print(sentence.formula())

knowledge = And(Implication(Not(rain), hagrid),
                Or(hagrid, dumbledore),
                Not(And(hagrid, dumbledore)),
                dumbledore
                )

print(model_check(knowledge, rain ))
#print(knowledge.formula())