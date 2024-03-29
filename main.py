# Initialistation globale
import os
os.system('cls')
print("Chargement..")

from colorama import Fore, init, Back, Style

# Initialisation des variables
chess_board = [
    ['t', 'c', 'f', 'd', 'r', 'f', 'c', 't'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['·', '·', '·', '·', '·', '·', '·', '·'],
    ['·', '·', '·', '·', '·', '·', '·', '·'],
    ['·', '·', '·', '·', '·', '·', '·', '·'],
    ['·', '·', '·', '·', '·', '·', '·', '·'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['T', 'C', 'F', 'D', 'R', 'F', 'C', 'T']
]

chess_display = "" # contient l'echiqier lisible pour un humain
user1 = "" # contient le nom du joueur 1
user2 = "" # contient le nom du joueur 2
coup = "    " # contient le coup actuel du tour
end_game = False  # Pour savoir si la game est finie
winner = ""  # Pour savoir qui est le gagant à la fin
tour = 0  # Pour savoir le tour de qui c'est et le nombre de tour effectué depuis le début de la partie
trace = []  # Contient l'historique de la partie
player = "" # Indique la couleur du joueur actuel
selection = "" # Position de la selection de l'utilisateur (e5)
selection_indice = "" #Position de la selection de l'utilisateur en indice (54)
selection_tuple = "" # Position de la selection de l'utilisateur en tuple (5, 4)
pion = "" # Pion actuellement utilisé
coup_possible = [] # Contient la liste des coups possible en fonction du pion séléctionné et de sa position

init()

# Affiche le tableau de jeu
def display_game(player, selection, pion):
    global chess_board
    chess_display = ""
    num = 1
    for x in range(len(chess_board)):
        for y in range(len(chess_board[0])):  
            try:
                if chess_board[x][y][1] == 'e':
                    chess_display += Fore.GREEN + chess_board[x][y][0] + " " + Style.RESET_ALL
            except:
                if x == selection[0] and y == selection[1]:
                    chess_display += Fore.BLUE + Style.BRIGHT + chess_board[x][y][0] + " " + Style.RESET_ALL
                elif chess_board[x][y][0] == '·':
                    # Si le caractère est un point médian, le rendre rouge
                    chess_display += Fore.RED + chess_board[x][y][0] + " " + Style.RESET_ALL
                elif player == "WHITE" and chess_board[x][y][0].islower() or player == "BLACK" and chess_board[x][y].isupper():
                    # Si le caractère est une lettre minuscule et que l'utilisateur est WHITE ou inversement, le rendre rouge
                    chess_display += Fore.RED + chess_board[x][y][0] + " " + Style.RESET_ALL
                else:
                    # Sinon, ajouter le caractère normal
                    chess_display += chess_board[x][y][0] + " "         
        chess_display +=  "  " + Style.BRIGHT + Fore.YELLOW + str(num) + Style.RESET_ALL + "\n"
        num += 1
    print("Voici le tableau de jeu de ce tour :")
    print("\n")
    print(Fore.YELLOW + Style.BRIGHT + "a b c d e f g h" + Style.RESET_ALL)
    print("\n")
    print(chess_display)

def verification_pion(pion, player):
    try:
        if not pion[0] in "abcdefghABCDEFGH":
            return [False,"La lettre n'est pas valide !", ""]
        if not pion[1] in "123456678":
            return [False,"Le chiffre n'est pas valide !", ""]
    except:
        return [False,"Erreur inconnue !", ""]
    row = int(pion[1]) - 1  # Convertit la rangée en indice (5 -> 4)
    col = ord(pion[0]) - ord('a')  # Convertit la colonne en indice (e -> 4)
    pion = chess_board[row][col]

    if pion == "·":
        return [False,"Aucun pion sur la position demandée !", ""]

    if player == "WHITE":
        if not pion in "TCFDRP":
            return [False,"Le pion sélectionné ne vous appartient pas !", ""]
        else: 
            if (pion == "T"):
                pion = "tour"
            elif (pion == "C"):
                pion = "Chevalier"
            elif (pion == "F"):
                pion = "Fou"
            elif (pion == "D"):
                pion = "Dame"
            elif (pion == "R"):
                pion = "Roi"
            else:
                pion = "Pion"
            return [True,"Pion valide !", pion]
    else:
        if not pion in "tcfdrp":
            return [False,"Le pion sélectionné ne vous appartient pas !", ""]
        else: 
            if (pion == "t"):
                pion = "tour"
            elif (pion == "c"):
                pion = "Chevalier"
            elif (pion == "f"):
                pion = "Fou"
            elif (pion == "d"):
                pion = "Dame"
            elif (pion == "r"):
                pion = "Roi"
            else:
                pion = "Pion"
            return [True,"Pion valide !", pion]
        
def verification_coup(coup):
    if not coup[3] in "abcdefghABCDEFGH":
        return [False,"La lettre n'est pas valide !", ""]
    if not coup[4] in "123456678":
        return [False,"Le chiffre n'est pas valide !", ""]
    row = int(coup[4]) - 1  # Convertit la rangée en indice (5 -> 4)
    col = ord(coup[3]) - ord('a')  # Convertit la colonne en indice (e -> 4)
    
    # On regarde si la case demandée est atteignable par le pion, sinon on return False
    try:
        if chess_board[row][col][1] == "e":
            return [True,"Changement possible !", ""]
    except:
        return [False,"Le chiffre n'est pas valide !", ""]

def joue_le_coup(coup):
    row_depart = int(coup[1]) - 1  # Convertit la rangée en indice (5 -> 4)
    col_depart = ord(coup[0]) - ord('a')  # Convertit la colonne en indice (e -> 4)
    row_final = int(coup[4]) - 1  # Convertit la rangée en indice (5 -> 4)
    col_final = ord(coup[3]) - ord('a')  # Convertit la colonne en indice (e -> 4)
    pion = chess_board[row_depart][col_depart]

    chess_board[row_final][col_final] = pion
    chess_board[row_depart][col_depart] = "·"

def chess_reset():
    for x in range(len(chess_board)):
        for y in range(len(chess_board[0])):
            try:
                chess_board[x][y] = chess_board[x][y][0]
            except:
                pass


def generation_coup_possible(player, pion, position):
    global chess_board
    
    if player == "WHITE":
        if pion == "Pion":
            if position[0] > 0: # Vérifie si le pion est sur la première rangée (i.e. ne peut pas aller en arrière)
                if chess_board[position[0] - 1][position[1]] == "·":
                    chess_board[position[0] - 1][position[1]] += "e" # On ajoute "e" à la case quand elle est un coup possible
                if position[0] == 6 and chess_board[position[0] - 2][position[1]] == "·": # Si c'est le premier tour du pion
                    chess_board[position[0] - 2][position[1]] += "e" 
                if position[1] < 7 and chess_board[position[0] - 1][position[1] + 1].islower(): # Si il y a un pion à la diagonale droite
                    chess_board[position[0] - 1][position[1] + 1] += "e"
                if position[1] > 0 and chess_board[position[0] - 1][position[1] - 1].islower(): # Si il y a un pion à la diagonale gauche
                    chess_board[position[0] - 1][position[1] - 1] += "e"
        if pion == "Chevalier":
            # Position du chevalier
            chevalier_row, chevalier_col = position

            # Liste des mouvements possibles du chevalier
            possible_moves = [(chevalier_row+2, chevalier_col+1), (chevalier_row+2, chevalier_col-1),
                            (chevalier_row-2, chevalier_col+1), (chevalier_row-2, chevalier_col-1),
                            (chevalier_row+1, chevalier_col+2), (chevalier_row+1, chevalier_col-2),
                            (chevalier_row-1, chevalier_col+2), (chevalier_row-1, chevalier_col-2)]

            # Pour chaque mouvement possible, vérifie si la position est valide et ajoute un "e" si oui
            for move in possible_moves:
                row, col = move
                if 0 <= row < len(chess_board) and 0 <= col < len(chess_board[0]):
                    if chess_board[row][col] == "·" or chess_board[row][col].islower():
                        chess_board[row][col] += "e"
        if pion == "Tour":
            # Position de la tour
            tour_row, tour_col = position

            # Vérifie les mouvements possibles vers le haut
            for row in range(tour_row - 1, -1, -1):
                if chess_board[row][tour_col] == "·":
                    chess_board[row][tour_col] += "e"
                elif chess_board[row][tour_col].islower():
                    chess_board[row][tour_col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers le bas
            for row in range(tour_row + 1, len(chess_board)):
                if chess_board[row][tour_col] == "·":
                    chess_board[row][tour_col] += "e"
                elif chess_board[row][tour_col].islower():
                    chess_board[row][tour_col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers la droite
            for col in range(tour_col + 1, len(chess_board[0])):
                if chess_board[tour_row][col] == "·":
                    chess_board[tour_row][col] += "e"
                elif chess_board[tour_row][col].islower():
                    chess_board[tour_row][col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers la gauche
            for col in range(tour_col - 1, -1, -1):
                if chess_board[tour_row][col] == "·":
                    chess_board[tour_row][col] += "e"
                elif chess_board[tour_row][col].islower():
                    chess_board[tour_row][col] += "e"
                    break
                else:
                    break
        if pion == "Fou":
            # Position du fou
            fou_row, fou_col = position

            # Liste des mouvements possibles du fou (en diagonale)
            possible_moves = []

            # Ajoute tous les mouvements possibles dans la même diagonale vers la droite et vers le bas
            for i in range(1, min(len(chess_board) - fou_row, len(chess_board[0]) - fou_col)):
                if chess_board[fou_row+i][fou_col+i] == "·":
                    possible_moves.append((fou_row+i, fou_col+i))
                elif chess_board[fou_row+i][fou_col+i].islower():
                    possible_moves.append((fou_row+i, fou_col+i))
                    break  # Arrête la boucle si on rencontre une pièce ennemie
                else:
                    break  # Arrête la boucle si on rencontre une pièce alliée

            # Ajoute tous les mouvements possibles dans la même diagonale vers la droite et vers le haut
            for i in range(1, min(fou_row+1, len(chess_board[0]) - fou_col)):
                if chess_board[fou_row-i][fou_col+i] == "·":
                    possible_moves.append((fou_row-i, fou_col+i))
                elif chess_board[fou_row-i][fou_col+i].islower():
                    possible_moves.append((fou_row-i, fou_col+i))
                    break
                else:
                   break

            # Ajoute tous les mouvements possibles dans la même diagonale vers la gauche et vers le bas
            for i in range(1, min(len(chess_board) - fou_row, fou_col+1)):
                if chess_board[fou_row+i][fou_col-i] == "·":
                    possible_moves.append((fou_row+i, fou_col-i))
                elif chess_board[fou_row+i][fou_col-i].islower():
                    possible_moves.append((fou_row+i, fou_col-i))
                    break
                else:
                    break

            # Ajoute tous les mouvements possibles dans la même diagonale vers la gauche et vers le haut
            for i in range(1, min(fou_row+1, fou_col+1)):
                if chess_board[fou_row-i][fou_col-i] == "·":
                    possible_moves.append((fou_row-i, fou_col-i))
                elif chess_board[fou_row-i][fou_col-i].islower():
                    possible_moves.append((fou_row-i, fou_col-i))
                    break
                else:
                    break

            # Pour chaque mouvement possible, vérifie si la position est valide et ajoute un "e" si oui
            for move in possible_moves:
                row, col = move
                if 0 <= row < len(chess_board) and 0 <= col < len(chess_board[0]):
                    if chess_board[row][col] == "·" or chess_board[row][col].islower():
                        chess_board[row][col] += "e"
        if pion == "Dame":
            # Position de la dame
            dame_row, dame_col = position

            # Liste des mouvements possibles de la dame (combinaison de la tour et du fou)
            possible_moves = []

            # Vérifie les mouvements possibles vers le haut
            for row in range(dame_row - 1, -1, -1):
                if chess_board[row][dame_col] == "·":
                    chess_board[row][dame_col] += "e"
                elif chess_board[row][dame_col].islower():
                    chess_board[row][dame_col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers le bas
            for row in range(dame_row + 1, len(chess_board)):
                if chess_board[row][dame_col] == "·":
                    chess_board[row][dame_col] += "e"
                elif chess_board[row][dame_col].islower():
                    chess_board[row][dame_col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers la droite
            for col in range(dame_col + 1, len(chess_board[0])):
                if chess_board[dame_row][col] == "·":
                    chess_board[dame_row][col] += "e"
                elif chess_board[dame_row][col].islower():
                    chess_board[dame_row][col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers la gauche
            for col in range(dame_col - 1, -1, -1):
                if chess_board[dame_row][col] == "·":
                    chess_board[dame_row][col] += "e"
                elif chess_board[dame_row][col].islower():
                    chess_board[dame_row][col] += "e"
                    break
                else:
                    break

            # Ajoute tous les mouvements possibles du fou (en diagonale)
            for i in range(1, min(len(chess_board) - dame_row, len(chess_board[0]) - dame_col)):
                if chess_board[dame_row+i][dame_col+i] == "·":
                    possible_moves.append((dame_row+i, dame_col+i))
                elif chess_board[dame_row+i][dame_col+i].islower():
                    possible_moves.append((dame_row+i, dame_col+i))
                    break
                else:
                    break
            for i in range(1, min(dame_row+1, len(chess_board[0]) - dame_col)):
                if chess_board[dame_row-i][dame_col+i] == "·":
                    possible_moves.append((dame_row-i, dame_col+i))
                elif chess_board[dame_row-i][dame_col+i].islower():
                    possible_moves.append((dame_row-i, dame_col+i))
                    break
                else:
                    break
            for i in range(1, min(len(chess_board) - dame_row, dame_col+1)):
                if chess_board[dame_row+i][dame_col-i] == "·":
                    possible_moves.append((dame_row+i, dame_col-i))
                elif chess_board[dame_row+i][dame_col-i].islower():
                    possible_moves.append((dame_row+i, dame_col-i))
                    break
                else:
                    break
            for i in range(1, min(dame_row+1, dame_col+1)):
                if chess_board[dame_row-i][dame_col-i] == "·":
                    possible_moves.append((dame_row-i, dame_col-i))
                elif chess_board[dame_row-i][dame_col-i].islower():
                    possible_moves.append((dame_row-i, dame_col-i))
                    break
                else:
                    break

            # Pour chaque mouvement possible, vérifie si la position est valide et ajoute un "e" si oui
            for move in possible_moves:
                row, col = move
                if 0 <= row < len(chess_board) and 0 <= col < len(chess_board[0]):
                    if chess_board[row][col] == "·" or chess_board[row][col].islower():
                        chess_board[row][col] += "e"
        if pion == "Roi":
            # Position du roi
            king_row, king_col = position

            # Liste des mouvements possibles du roi
            possible_moves = []

            # Parcours des cases adjacentes au roi
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Si le mouvement ne change pas la position du roi, on passe au suivant
                    if i == 0 and j == 0:
                        continue
                    # Coordonnées de la case adjacente
                    row, col = king_row + i, king_col + j
                    # Si la case est en dehors de l'échiquier, on passe au suivant
                    if row < 0 or row >= len(chess_board) or col < 0 or col >= len(chess_board[row]):
                        continue
                    # Si la case est vide ou contient une pièce ennemie, on ajoute le mouvement aux coups possibles
                    if chess_board[row][col] == "·" or chess_board[row][col].islower():
                        possible_moves.append((row, col))
                        chess_board[row][col] += "e"
    else:
        if pion == "Pion":
            if position[0] > 0: # Vérifie si le pion est sur la première rangée (i.e. ne peut pas aller en arrière)
                if chess_board[position[0] - 1][position[1]] == "·":
                    chess_board[position[0] - 1][position[1]] += "e" # On ajoute "e" à la case quand elle est un coup possible
                if position[0] == 6 and chess_board[position[0] - 2][position[1]] == "·": # Si c'est le premier tour du pion
                    chess_board[position[0] - 2][position[1]] += "e" 
                if position[1] < 7 and chess_board[position[0] - 1][position[1] + 1].isupper(): # Si il y a un pion à la diagonale droite
                    chess_board[position[0] - 1][position[1] + 1] += "e"
                if position[1] > 0 and chess_board[position[0] - 1][position[1] - 1].isupper(): # Si il y a un pion à la diagonale gauche
                    chess_board[position[0] - 1][position[1] - 1] += "e"
        if pion == "Chevalier":
            # Position du chevalier
            chevalier_row, chevalier_col = position

            # Liste des mouvements possibles du chevalier
            possible_moves = [(chevalier_row+2, chevalier_col+1), (chevalier_row+2, chevalier_col-1),
                            (chevalier_row-2, chevalier_col+1), (chevalier_row-2, chevalier_col-1),
                            (chevalier_row+1, chevalier_col+2), (chevalier_row+1, chevalier_col-2),
                            (chevalier_row-1, chevalier_col+2), (chevalier_row-1, chevalier_col-2)]

            # Pour chaque mouvement possible, vérifie si la position est valide et ajoute un "e" si oui
            for move in possible_moves:
                row, col = move
                if 0 <= row < len(chess_board) and 0 <= col < len(chess_board[0]):
                    if chess_board[row][col] == "·" or chess_board[row][col].isupper():
                        chess_board[row][col] += "e"
        if pion == "Tour":
            # Position de la tour
            tour_row, tour_col = position

            # Vérifie les mouvements possibles vers le haut
            for row in range(tour_row - 1, -1, -1):
                if chess_board[row][tour_col] == "·":
                    chess_board[row][tour_col] += "e"
                elif chess_board[row][tour_col].isupper():
                    chess_board[row][tour_col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers le bas
            for row in range(tour_row + 1, len(chess_board)):
                if chess_board[row][tour_col] == "·":
                    chess_board[row][tour_col] += "e"
                elif chess_board[row][tour_col].isupper():
                    chess_board[row][tour_col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers la droite
            for col in range(tour_col + 1, len(chess_board[0])):
                if chess_board[tour_row][col] == "·":
                    chess_board[tour_row][col] += "e"
                elif chess_board[tour_row][col].isupper():
                    chess_board[tour_row][col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers la gauche
            for col in range(tour_col - 1, -1, -1):
                if chess_board[tour_row][col] == "·":
                    chess_board[tour_row][col] += "e"
                elif chess_board[tour_row][col].isupper():
                    chess_board[tour_row][col] += "e"
                    break
                else:
                    break
        if pion == "Fou":
            # Position du fou
            fou_row, fou_col = position

            # Liste des mouvements possibles du fou (en diagonale)
            possible_moves = []

            # Ajoute tous les mouvements possibles dans la même diagonale vers la droite et vers le bas
            for i in range(1, min(len(chess_board) - fou_row, len(chess_board[0]) - fou_col)):
                if chess_board[fou_row+i][fou_col+i] == "·":
                    possible_moves.append((fou_row+i, fou_col+i))
                elif chess_board[fou_row+i][fou_col+i].isupper():
                    possible_moves.append((fou_row+i, fou_col+i))
                    break  # Arrête la boucle si on rencontre une pièce ennemie
                else:
                    break  # Arrête la boucle si on rencontre une pièce alliée

            # Ajoute tous les mouvements possibles dans la même diagonale vers la droite et vers le haut
            for i in range(1, min(fou_row+1, len(chess_board[0]) - fou_col)):
                if chess_board[fou_row-i][fou_col+i] == "·":
                    possible_moves.append((fou_row-i, fou_col+i))
                elif chess_board[fou_row-i][fou_col+i].isupper():
                    possible_moves.append((fou_row-i, fou_col+i))
                    break
                else:
                   break

            # Ajoute tous les mouvements possibles dans la même diagonale vers la gauche et vers le bas
            for i in range(1, min(len(chess_board) - fou_row, fou_col+1)):
                if chess_board[fou_row+i][fou_col-i] == "·":
                    possible_moves.append((fou_row+i, fou_col-i))
                elif chess_board[fou_row+i][fou_col-i].isupper():
                    possible_moves.append((fou_row+i, fou_col-i))
                    break
                else:
                    break

            # Ajoute tous les mouvements possibles dans la même diagonale vers la gauche et vers le haut
            for i in range(1, min(fou_row+1, fou_col+1)):
                if chess_board[fou_row-i][fou_col-i] == "·":
                    possible_moves.append((fou_row-i, fou_col-i))
                elif chess_board[fou_row-i][fou_col-i].isupper():
                    possible_moves.append((fou_row-i, fou_col-i))
                    break
                else:
                    break

            # Pour chaque mouvement possible, vérifie si la position est valide et ajoute un "e" si oui
            for move in possible_moves:
                row, col = move
                if 0 <= row < len(chess_board) and 0 <= col < len(chess_board[0]):
                    if chess_board[row][col] == "·" or chess_board[row][col].isupper():
                        chess_board[row][col] += "e"
        if pion == "Dame":
            # Position de la dame
            dame_row, dame_col = position

            # Liste des mouvements possibles de la dame (combinaison de la tour et du fou)
            possible_moves = []

            # Vérifie les mouvements possibles vers le haut
            for row in range(dame_row - 1, -1, -1):
                if chess_board[row][dame_col] == "·":
                    chess_board[row][dame_col] += "e"
                elif chess_board[row][dame_col].isupper():
                    chess_board[row][dame_col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers le bas
            for row in range(dame_row + 1, len(chess_board)):
                if chess_board[row][dame_col] == "·":
                    chess_board[row][dame_col] += "e"
                elif chess_board[row][dame_col].isupper():
                    chess_board[row][dame_col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers la droite
            for col in range(dame_col + 1, len(chess_board[0])):
                if chess_board[dame_row][col] == "·":
                    chess_board[dame_row][col] += "e"
                elif chess_board[dame_row][col].isupper():
                    chess_board[dame_row][col] += "e"
                    break
                else:
                    break

            # Vérifie les mouvements possibles vers la gauche
            for col in range(dame_col - 1, -1, -1):
                if chess_board[dame_row][col] == "·":
                    chess_board[dame_row][col] += "e"
                elif chess_board[dame_row][col].isupper():
                    chess_board[dame_row][col] += "e"
                    break
                else:
                    break

            # Ajoute tous les mouvements possibles du fou (en diagonale)
            for i in range(1, min(len(chess_board) - dame_row, len(chess_board[0]) - dame_col)):
                if chess_board[dame_row+i][dame_col+i] == "·":
                    possible_moves.append((dame_row+i, dame_col+i))
                elif chess_board[dame_row+i][dame_col+i].isupper():
                    possible_moves.append((dame_row+i, dame_col+i))
                    break
                else:
                    break
            for i in range(1, min(dame_row+1, len(chess_board[0]) - dame_col)):
                if chess_board[dame_row-i][dame_col+i] == "·":
                    possible_moves.append((dame_row-i, dame_col+i))
                elif chess_board[dame_row-i][dame_col+i].isupper():
                    possible_moves.append((dame_row-i, dame_col+i))
                    break
                else:
                    break
            for i in range(1, min(len(chess_board) - dame_row, dame_col+1)):
                if chess_board[dame_row+i][dame_col-i] == "·":
                    possible_moves.append((dame_row+i, dame_col-i))
                elif chess_board[dame_row+i][dame_col-i].isupper():
                    possible_moves.append((dame_row+i, dame_col-i))
                    break
                else:
                    break
            for i in range(1, min(dame_row+1, dame_col+1)):
                if chess_board[dame_row-i][dame_col-i] == "·":
                    possible_moves.append((dame_row-i, dame_col-i))
                elif chess_board[dame_row-i][dame_col-i].isupper():
                    possible_moves.append((dame_row-i, dame_col-i))
                    break
                else:
                    break

            # Pour chaque mouvement possible, vérifie si la position est valide et ajoute un "e" si oui
            for move in possible_moves:
                row, col = move
                if 0 <= row < len(chess_board) and 0 <= col < len(chess_board[0]):
                    if chess_board[row][col] == "·" or chess_board[row][col].isupper():
                        chess_board[row][col] += "e"
        if pion == "Roi":
            # Position du roi
            king_row, king_col = position

            # Liste des mouvements possibles du roi
            possible_moves = []

            # Parcours des cases adjacentes au roi
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Si le mouvement ne change pas la position du roi, on passe au suivant
                    if i == 0 and j == 0:
                        continue
                    # Coordonnées de la case adjacente
                    row, col = king_row + i, king_col + j
                    # Si la case est en dehors de l'échiquier, on passe au suivant
                    if row < 0 or row >= len(chess_board) or col < 0 or col >= len(chess_board[row]):
                        continue
                    # Si la case est vide ou contient une pièce ennemie, on ajoute le mouvement aux coups possibles
                    if chess_board[row][col] == "·" or chess_board[row][col].isupper():
                        possible_moves.append((row, col))
                        chess_board[row][col] += "e"

def chess_check():
    global chess_board
    white_roi = False
    black_roi = False
    for x in range(len(chess_board)):
        for y in range(len(chess_board[0])):
            if chess_board[x][y] == "R":
                white_roi = True
            if chess_board[x][y] == "r":
                black_roi = True

    os.system("cls")
    if white_roi == False:
        winner = "BLACK"
        end_game = True
        print("LES NOIRS ONT GAGNEE !!")

    if black_roi == False:
        winner = "WHITE"
        end_game = True
        print("LES BLANCS ONT GAGNEE !!")    


os.system('cls')
print("Bienvenue dans un jeu d'échec !")

# Enregistrement des noms d'utilisateur
user1 = input("Nom de l'utilisateur n°1 ?")
user2 = input("Nom de l'utilisateur n°2 ?")

os.system('cls')

print(user1 + " vous êtes les " + Fore.WHITE + "blancs" + Style.RESET_ALL + ", vous posséder les pions en majuscules, " +
      user2 + " vous êtes les " + Fore.BLACK + "noirs" + Style.RESET_ALL + ", vous posséder les pions en minuscules.")

while end_game == False:
    coup = '    '
    selection = "99"
    os.system("cls")
    if tour % 2 == 0:
        player = "WHITE"
    else:
        player = "BLACK"
    
    display_game(player, selection, "")
    print(Fore.RED + "Non sélectionnable  " + Fore.BLUE + "Actuellement sélectionné  " + Fore.GREEN + "Coup possible" + Style.RESET_ALL)
    if player == "WHITE":
        selection = input("C'est au tour des Blancs, quel pion voulez vous jouer ? (ex: e5)")
    else:
        selection = input("C'est au tour des Noirs, quel pion voulez vous jouer ? (ex: e5)")

    while verification_pion(selection, player)[0] == False:
        selection = "99"
        os.system("cls")
        print(Fore.RED + "a b c d e f g h" + Style.RESET_ALL)
        print("\n")
        display_game(player, selection, "")
        print(Fore.RED + "Non sélectionnable  " + Fore.BLUE + "Actuellement sélectionné  " + Fore.GREEN + "Coup possible" + Style.RESET_ALL)
        selection = input(verification_pion(selection, player)[1] + " Quel pion voulez vous jouer ? (ex: e5)")
    
    selection_indice = str(int(selection[1]) - 1) + str(ord(selection[0]) - ord('a'))
    selection_tuple = tuple(map(int, str(selection_indice)))
    pion = verification_pion(selection, player)[2]
    generation_coup_possible(player, pion, selection_tuple)
    display_game(player, selection_tuple, pion)

    print(Fore.RED + "Non sélectionnable  " + Fore.BLUE + "Actuellement sélectionné  " + Fore.GREEN + "Coup possible" + Style.RESET_ALL)
    coup = selection +  " " + input("Où voulez vous le déplacer ?")

    while verification_coup(coup) == False:
        os.system("cls")
        print(Fore.RED + "a b c d e f g h" + Style.RESET_ALL)
        print("\n")
        display_game(player, selection_tuple, "")
        print(Fore.RED + "Non sélectionnable  " + Fore.BLUE + "Actuellement sélectionné  " + Fore.GREEN + "Coup possible" + Style.RESET_ALL)
        coup = selection +  " " + input("Vous ne pouvez pas déplacer votre pion sur cette case, une autre position ?")   

    joue_le_coup(coup)
    chess_reset()
    chess_board = list(reversed(chess_board))
    tour += 1
    chess_check()