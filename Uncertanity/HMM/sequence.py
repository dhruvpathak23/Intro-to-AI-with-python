from model import model

#Observed data
observations = [
    "umbrella",
    "umbrella",
    "no umbrella",
    "umbrella",
    "umbrella",
    "umbrella",
    "no umbrella",
    "no umbrella",
]

#predict underlying states
predictions = model.predict(observations)
for prediction in predictions:
    print(model.states[prediction].name)  