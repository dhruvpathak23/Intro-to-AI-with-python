import itertools


class Sentence:
    """
    Base class for all logical sentences.
    """

    def evaluate(self, model):
        raise Exception("Nothing to evaluate")

    def formula(self):
        return ""

    def symbols(self):
        return set()

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("Must be a logical sentence")

    @classmethod
    def parenthesize(cls, s):

        def balanced(s):
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0

        if (
            not s
            or s.isalpha()
            or (s[0] == "(" and s[-1] == ")" and balanced(s[1:-1]))
        ):
            return s

        return f"({s})"


class Symbol(Sentence):
    """
    Represents a propositional symbol (variable).
    """

    def __init__(self, name):
        self.name = name

    def evaluate(self, model):
        return model[self]

    def formula(self):
        return self.name

    def symbols(self):
        return {self}

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Not(Sentence):
    """
    Logical negation: ¬A
    """

    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def formula(self):
        return f"¬{Sentence.parenthesize(self.operand.formula())}"

    def symbols(self):
        return self.operand.symbols()


class And(Sentence):
    """
    Logical AND: A ∧ B ∧ ...
    """

    def __init__(self, *conjuncts):
        for c in conjuncts:
            Sentence.validate(c)
        self.conjuncts = list(conjuncts)

    def add(self, Sentence):
        Sentence.validate(Sentence)
        self.conjuncts.append(Sentence)

    def evaluate(self, model):
        return all(c.evaluate(model) for c in self.conjuncts)

    def formula(self):
        return " ∧ ".join(
            Sentence.parenthesize(c.formula()) for c in self.conjuncts
        )

    def symbols(self):
        return set().union(*(c.symbols() for c in self.conjuncts))


class Or(Sentence):
    """
    Logical OR: A ∨ B ∨ ...
    """

    def __init__(self, *disjuncts):
        for d in disjuncts:
            Sentence.validate(d)
        self.disjuncts = list(disjuncts)

    def evaluate(self, model):
        return any(d.evaluate(model) for d in self.disjuncts)

    def formula(self):
        return " ∨ ".join(
            Sentence.parenthesize(d.formula()) for d in self.disjuncts
        )

    def symbols(self):
        return set().union(*(d.symbols() for d in self.disjuncts))


class Implication(Sentence):
    """
    Logical implication: A → B
    """

    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def evaluate(self, model):
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def formula(self):
        return (
            f"{Sentence.parenthesize(self.antecedent.formula())} → "
            f"{Sentence.parenthesize(self.consequent.formula())}"
        )

    def symbols(self):
        return self.antecedent.symbols().union(self.consequent.symbols())


class Biconditional(Sentence):
    """
    Logical biconditional: A ↔ B
    """

    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def evaluate(self, model):
        return self.left.evaluate(model) == self.right.evaluate(model)

    def formula(self):
        return (
            f"{Sentence.parenthesize(self.left.formula())} ↔ "
            f"{Sentence.parenthesize(self.right.formula())}"
        )

    def symbols(self):
        return self.left.symbols().union(self.right.symbols())


class KnowledgeBase:
    """
    Stores known logical sentences.
    """

    def __init__(self):
        self.sentences = []

    def tell(self, sentence):
        Sentence.validate(sentence)
        self.sentences.append(sentence)

    def symbols(self):
        return set().union(*(s.symbols() for s in self.sentences))


# MODEL CHECKING ALGORITHM


def model_check(knowledge, query):
    """
    Returns True if knowledge base entails query.
    """

    def check_all(knowledge, query, symbols, model):
        """
        Recursive model-checking algorithm.
        """

        # If model has an assignment for each symbol
        if not symbols:
            # If KB is true in this model, query must be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else: 

            # Choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()

            # Create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True

            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            # Ensure entailment holds in both model
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    # Get all symbols in both Knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())
