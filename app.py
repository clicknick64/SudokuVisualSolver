from operator import ne
from random import sample
import csp
import time
import pygame


def draw_sudoku(screen, board):
    screen.fill(color)
    space = WIDTH/9
    for i in range(1,9):
        pygame.draw.line(screen, (0,0,0), (space*i,0), (space*i,600), 4 if i%3==0 else 2)
        pygame.draw.line(screen, (0,0,0), (0,space*i), (600, space*i), 4 if i%3==0 else 2)

    for i in range(9):
        for j in range(9):
            text_surface_obj = font_obj.render(str(board[i][j]), True, (0,0,0))
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (space*(i+0.5), space*(j+0.5))
            screen.blit(text_surface_obj, text_rect_obj)
    pygame.display.flip()

def print_sudoku(board):
    print("-"*37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")

def res_to_sudoku(res):
    formatted = []
    for i in range(9):
        for j in range(9):
            if (i,j) in res.keys():
                formatted.append(res[(i,j)])
            else:
                formatted.append(' ')
    formatted = [formatted[i*9:i*9+9] for i in range(9)]
    return formatted

# Test for valid values
def testCon(A, a, B, b):
    return a != b


# Forward Checking
def FC(cspProblem):
    a = solve(cspProblem, csp.mrv, csp.lcv, csp.forward_checking)
    return a

def solve(cspProblem, select_unassigned_variable=csp.first_unassigned_variable,
                        order_domain_values=csp.unordered_domain_values, inference=csp.no_inference):

    def backtrack(assignment):
        if len(assignment) == len(cspProblem.variables):
            return assignment
        var = select_unassigned_variable(assignment, cspProblem)
        for value in order_domain_values(var, assignment, cspProblem):
            if 0 == cspProblem.nconflicts(var, value, assignment):
                cspProblem.assign(var, value, assignment)
                draw_sudoku(screen, res_to_sudoku({**initial, **assignment}))
                if all(x in assignment for x in initial) and select_unassigned_variable==csp.mrv: 
                    time.sleep(0.2)
                    pass
                elif select_unassigned_variable == csp.first_unassigned_variable:
                    time.sleep(0.05)
                    pass
                removals = cspProblem.suppose(var, value)
                if inference(cspProblem, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                cspProblem.restore(removals)
        cspProblem.unassign(var, assignment)
        return None

    initial = {}

    for v in cspProblem.variables:
        if len(cspProblem.domains.get(v)) == 1:
            cspProblem.assign(v, cspProblem.domains.get(v)[0], initial)

    draw_sudoku(screen, res_to_sudoku(initial))
    time.sleep(1)

    result = backtrack({})
    return result


input_sudoku = input("Enter sudoku:")
if not input_sudoku: input_sudoku = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'

win = pygame.display.set_mode((600,600))
pygame.font.init()



# Set variables
variables = []
for i in range(9):
    for j in range(9):
        variables.append((j, i))

# Set domains
domains = {}
for i in range(9):
    for j in range(9):
        domains[(i, j)] = [v for v in range(1, 10)]

# Refine domains
for x,v in enumerate(input_sudoku.strip()):
    num = int(v)
    if num==0: continue
    i = x%9
    j = x//9
    domains[(i,j)] = [num]


# Set neighbors
neighbors = {}
for i in range(9):
    for j in range(9):
        neighbors[(i,j)] = []
        for h in range(9):
            if (i, h) != (i, j):
                neighbors[(i, j)].append((i, h))
            if (i, h) != (i, j):
                neighbors[(i, j)].append((h, j))
        corner = (i//3, j//3)
        for a in range(3):
            for b in range(3):
                if (corner[0]*3+a, corner[1]*3+b) != (i, j) and not (corner[0]*3+a, corner[1]*3+b) in neighbors[(i,j)]:
                    neighbors[(i,j)].append((corner[0]*3+a, corner[1]*3+b))


WIDTH = 600
  
# Initializing Pygame 
pygame.init() 
  
# Initializing surface 
screen = pygame.display.set_mode((WIDTH,WIDTH)) 

# Initialing RGB Color  
color = (255, 255, 255) 
  
font_obj = pygame.font.Font('freesansbold.ttf', 32)

cspProblem = csp.CSP(variables, domains, neighbors, testCon)
res = FC(cspProblem)

# Results
solved = res_to_sudoku(res)

draw_sudoku(screen, solved)


running = True
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
            pygame.quit()
