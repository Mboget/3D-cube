import subprocess
import sys
import os

def install_dependencies():
    """Installs dependencies from requirements.txt if they are missing."""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_file):
        print("Checking and installing dependencies...")
        try:
            # pip install -r requirements.txt handles checking if packages are already installed
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
    else:
        print("requirements.txt not found.")

# Run dependency check before importing other modules
install_dependencies()

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Définition des sommets du cube
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

# Définition des faces (groupes de 4 sommets)
surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

# Définition des couleurs pour chaque sommet (ou face)
colors = (
    (1, 0, 0), # Rouge
    (0, 1, 0), # Vert
    (0, 0, 1), # Bleu
    (1, 1, 0), # Jaune
    (1, 0, 1), # Magenta
    (0, 1, 1), # Cyan
    (1, 1, 1), # Blanc
    (0, 0, 0), # Noir
)

# Couleurs spécifiques pour chaque face
face_colors = (
    (1, 0, 0), # Face 1: Rouge
    (0, 1, 0), # Face 2: Vert
    (0, 0, 1), # Face 3: Bleu
    (1, 1, 0), # Face 4: Jaune
    (1, 0, 1), # Face 5: Magenta
    (0, 1, 1), # Face 6: Cyan
)

def Cube():
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(face_colors[i]) # Couleur de la face
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Optionnel : Dessiner les contours en noir pour mieux voir les arêtes
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3fv((0, 0, 0))
    edges = (
        (0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
        (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)
    )
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cube 3D Coloré - Contrôle Souris")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Activation du test de profondeur pour que les faces ne se superposent pas incorrectement
    glEnable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()
    
    mouse_down = False
    last_pos = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    last_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    x, y = pygame.mouse.get_pos()
                    dx = x - last_pos[0]
                    dy = y - last_pos[1]
                    last_pos = (x, y)
                    
                    glRotatef(dy, 1, 0, 0)
                    glRotatef(dx, 0, 1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        Cube()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
