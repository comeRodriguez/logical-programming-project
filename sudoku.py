from itertools import combinations
from typing import List, Tuple
import subprocess

#fonction pour passer d'une cellule d'un sudoku à un numéro de variable
def cell_to_variable(i: int, j: int, val: int) -> int:
    nombre = i * 81 + j * 9 + val
    return nombre

#fonction pour passer d'un numéro de variable à une cellule
def variable_to_cell(var: int) -> Tuple[int, int, int]:
    var = var - 1
    #On enlève -1 car on veut que le chiffre maximum dans la cellule soit 8 pour la ligne et la colonne
    ligne = var // 81
    #On fait la division entiere de var par 81 pour avoir le numéro de ligne
    var = var % 81
    #On met dans var le reste de la division euclidienne de var par 81
    colonne = var // 9
    #On fait la division entiere de var par 9 pour avoir le numéro de colonne
    var = var % 9
    #On met dans var le reste de la division euclidienne de var par 9
    valeur = var + 1
    #On rajoute plus un car on veut que le chiffre de la valeur soit compris entre 1 et 9
    return (ligne, colonne, valeur)


def at_least_one(vars: List[int]) -> List[int]:
    liste = vars[:]
    #On fait juste une copie de la liste donnée
    return liste


def unique(vars: List[int]) -> List[List[int]]:
    liste = []
    for a, b in combinations(vars, 2):
        liste.append([-a, -b])
        #On fait des combinaisons de 2 pour avoir chaque clauses
    return [vars] + liste


def create_cell_constraints() -> List[List[int]]:
    constraints = []
    variables: List[int] = []
    for ligne in range(9):
    #Pour chaque ligne
        for colonne in range(9):
        #Pour cahque colonne
            variables = []
            #On réinitialise notre liste a chaque fois pour éviter d'avoir des doublons
            for val in range(1, 10):
            #Pour chaque valeur
                variables.append(cell_to_variable(ligne, colonne, val))
                #On ajoute notre numero de variable à notre liste
            constraints += unique(variables)
            #On fait un unique sur la liste obtenue pour avoir nos contraintes sur chaque valeur

    return constraints
    #On retourne la liste


def create_line_constraints() -> List[List[int]]:
#Meme pensée que pour create_cell_constraints sauf qu'on utilise un at_least_one car on a déja mis la contrainte sur l'unicité
#Si on fait un unique, on va avoir des doublons
    constraints = []
    variables: List[int] = []
    for ligne in range(9):
        for val in range(1, 10):
            variables = []
            for colonne in range(9):
                variables.append(cell_to_variable(ligne, colonne, val))
            constraints += [at_least_one(variables)]

    return constraints


def create_column_constraints() -> List[List[int]]:
#Meme pensée que pour create_cell_constraints sauf qu'on utilise un at_least_one car on a déja mis la contrainte sur l'unicité
#Si on fait un unique, on va avoir des doublons
    constraints = []
    variables: List[int] = []
    for colonne in range(9):
        for val in range(1, 10):
            variables = []
            for ligne in range(9):
                variables.append(cell_to_variable(ligne, colonne, val))
            constraints += [at_least_one(variables)]

    return constraints


def create_box_constraints() -> List[List[int]]:
#Meme pensée que pour create_cell_constraints sauf qu'on utilise un at_least_one car on a déja mis la contrainte sur l'unicité
#Si on fait un unique, on va avoir des doublons
#Ici on a plein de boucles car on veut traiter les lignes, colonnes et cellules 3 par 3 (je pense qu'on peut simplifier)
    constraints = []
    variables: List[int] = []
    for val in range(1, 10):
        variables = []
        for line in range(3):
            for column in range(3):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]
    for val in range(1, 10):
        variables = []
        for line in range(3):
            for column in range(3, 6):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]
    for val in range(1, 10):
        variables = []
        for line in range(3):
            for column in range(6, 9):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]
    for val in range(1, 10):
        variables = []
        for line in range(3, 6):
            for column in range(3):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]
    for val in range(1, 10):
        variables = []
        for line in range(3, 6):
            for column in range(3, 6):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]
    for val in range(1, 10):
        variables = []
        for line in range(3, 6):
            for column in range(6, 9):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]
    for val in range(1, 10):
        variables = []
        for line in range(6, 9):
            for column in range(3):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]
    for val in range(1, 10):
        variables = []
        for line in range(6, 9):
            for column in range(3, 6):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]
    for val in range(1, 10):
        variables = []
        for line in range(6, 9):
            for column in range(6, 9):
                variables.append(cell_to_variable(line, column, val))
        constraints += [at_least_one(variables)]

    return constraints


def create_value_constraints(grid: List[List[int]]) -> List[List[int]]:
#Creattion des contraintes sur les contraintes de bases de notre liste
#Par exemple, on veut intégrer à nos contraintes le fait que 5 soit dans la premiere colonne de la premiere ligne
    constraints = []
    variables: List[List[int]] = []
    for position_line in range(9):
        for position_column in range(9):
            variables = []
            if grid[position_line][position_column] != 0:
                variables.append(
                    [
                        cell_to_variable(
                            position_line,
                            position_column,
                            grid[position_line][position_column],
                        )
                    ]
                )
            constraints += variables

    return constraints


def generate_problem(grid: List[List[int]]) -> List[List[int]]:
#On assemble ici nos fonctions pour mettre le tout dans une base de clauses
    clauses = create_cell_constraints()
    clauses_ligne = create_line_constraints()
    clauses_colonne = create_column_constraints()
    clauses_carre = create_box_constraints()
    clauses_valeur = create_value_constraints(grid)
    ClausesBase = (
        clauses + clauses_ligne + clauses_colonne + clauses_carre + clauses_valeur
    )
    return ClausesBase


def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) -> str:
#On génère le code DIMACS
    phrase = f"p cnf {nb_vars} {len(clauses)}\n"
    for clause in range(len(clauses)):
        for variables in range(len(clauses[clause])):
            phrase += f"{clauses[clause][variables]} "
        phrase += f"0\n"

    return phrase


def write_dimacs_file(dimacs: str, filename: str):
#Fonction pour écrire dans le fichier
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def generate_dimacs_file(grid, filename: str):
#On crée le fichier et on écrit dedans
    write_dimacs_file((clauses_to_dimacs(generate_problem(grid), 729)), filename)


def exec_gophersat(
#Fonction donnée par le prof
    filename: str, cmd: str = "./gophersat-1.1.6", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:].split(" ")

    return True, [int(x) for x in model]


def model_to_grid(model: List[int], nb_vals: int = 9) -> List[List]:
#Fonction pour passer d'un model (ensemble de variables) à une grille de sudoku
#Fonction qui sera utilisée pour passer du résultat donnée par gophersat à la grille correspondante
    result = model
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    for variables in result:
        if variables > 0:
            valeur = variable_to_cell(variables)
            grid[valeur[0]][valeur[1]] = valeur[2]
    return grid


def display(grid: List[List[int]], nb_lines: int, nb_column: int):
#Fonction d'affichage de la grille
    print("  - - - - - - - - - - - - - - - - - - - - - - - - ")
    print()
    for line in range(9):
        print("|", end="")
        for column in range(9):
            if grid[line][column] == 0:
                print("  .  ", end="")
            if grid[line][column] != 0:
                print(" ", grid[line][column], " ", end="")
            if column == 2 or column == 5:
                print("| ", end="")
            if column == 8:
                print("|")
                print()
        if line == 2 or line == 5 or line == 8:
            print("  - - - - - - - - - - - - - - - - - - - - - - - - ")
            print()


Grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


Grid2 = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]

Grid3 = [
    [0, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 9],
]



generate_dimacs_file(Grid, "sudoku.cnf")
result = exec_gophersat("sudoku.cnf")
print()
print("Problème initial : ")
display(Grid, 9, 9)
print()
print()
print()
print()
print("Problème résolu : ")
display(model_to_grid(result[1]), 9, 9)
print()
print()
print()
print()
print()
print()
print()
generate_dimacs_file(Grid2, "sudoku2.cnf")
result2 = exec_gophersat("sudoku2.cnf")
print()
print("Problème initial : ")
display(Grid2, 9, 9)
print()
print()
print()
print()
print("Problème résolu : ")
display(model_to_grid(result2[1]), 9, 9)
print()
print()
print()
print()
print()
print()
print()
generate_dimacs_file(Grid3, "sudoku3.cnf")
result3 = exec_gophersat("sudoku3.cnf")
print()
print("Problème initial : ")
display(Grid3, 9, 9)
print()
print()
print()
print()
print("Problème résolu : ")
display(model_to_grid(result3[1]), 9, 9)
print(generate_problem(Grid))

