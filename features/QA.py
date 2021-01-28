import json
import random

with open ("./features/QA.json", "r", encoding="utf-8") as f :
    item = json.load(f)['questions']

def return_random_QA() :
    random_QA = item[random.randint(0, len(item)-1)]
    Q = random_QA['Question']
    A = random_QA['Answer']
    R = random_QA['Reference']
    return Q, A, R