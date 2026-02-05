import termcolor

from logic import *

musturd = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [musturd, plum, scarlet]

ballroom = Symbol("Ballroom")
kitchen = Symbol("Kitchen") 
library = Symbol("Library")
rooms = [ballroom, kitchen, library]

knife = Symbol("Knife")
revolver = Symbol("Revolver")
rope = Symbol("Rope")
weapons = [knife, revolver, rope]

symbols = characters + rooms + weapons

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}: YES", "green")

        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")

knowledge = And(
    Or(musturd, plum, scarlet),  # One of the three characters did it
    Or(ballroom, kitchen, library),  # The crime took place in one of the three rooms
    Or(knife, revolver, rope),  # The murder weapon was one of the three
) 
#print(knowledge.formula())

knowledge.add(Not(musturd))
knowledge.add(Not(kitchen))
knowledge.add(Not(revolver))

knowledge.add(Or(
   Not(scarlet), Not(library), Not(rope) 
))
knowledge.add(Not(plum))

knowledge.add(Not(ballroom))

check_knowledge(knowledge)
