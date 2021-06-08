from itertools import combinations
from typing import List, Tuple



def cell_to_variable(i: int, j: int, val: int) -> int:
    nombre = i * 81 + j * 9 + val
    return nombre


def variable_to_cell(var: int) -> Tuple[int, int, int]:
    var = var - 1
    ligne = var // 81
    var = var % 81
    colonne = var // 9
    var = var % 9
    valeur = var + 1
    return (ligne, colonne, valeur)





def at_least_one(vars: List[int]) -> List[int]:
    liste = vars[:]
    return liste




def create_box_constraints() -> List[List[int]]:
    constraints = []
    variables: List[int] = []
    range_number = (0, 3, 6, 9)
    for iterations in range(len(range_number)-1):
        for val in range(1, 10): 
            variables = []
            for line in range(range_number[iterations], range_number[iterations+1]):
                for iterations2 in range(len(range_number)-1):
                    for column in range(range_number[iterations2], range_number[iterations2+1]):
                        variables.append(cell_to_variable(line, column, val))
            constraints += [at_least_one(variables)]
    return constraints




print(create_box_constraints())