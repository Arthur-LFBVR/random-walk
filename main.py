# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


##############################################################################################################################
# Paramètres initiaux

n_step = 250       # Nombre d'itération
n_particle = 10    # Nombre de particule

proba_x = 0.5       # Probabilité de déplacement dans la direction x
proba_y = 0.5       # Probabilité de déplacement dans la direction x

a = 0.25            # Longueur de déplacement

L = 10              # Taille de la boite

box = False         # Présence de boite  
video = True       # Présence de la vidéo 
save_video = True #Sauvegarder la vidéo         


##############################################################################################################################
# Fonctions

# Conditions limites
def bound_condition(pos_x : float, pos_y : float):
    if (pos_x > L):
        pos_x -= 2*(pos_x-L)
    if (pos_x < -L):
        pos_x -= 2*(pos_x+L)
    if (pos_y > L):
        pos_y -= 2*(pos_y-L)
    if (pos_y < -L):
        pos_y -= 2*(pos_y+L)
    return pos_x, pos_y

# Mise à jour des positions des particules
def position_update(t : int, particles : list, n_particle : int):
    for p in range(0, n_particle):
        direction = np.random.choice([np.random.uniform(-(np.pi)/2, (np.pi)/2), np.random.uniform(0, np.pi), np.random.uniform((np.pi)/2, (3*np.pi)/2), np.random.uniform(np.pi, 2*np.pi)], \
                                    p=[proba_x/2, proba_y/2, (1-proba_x)/2, (1-proba_y)/2])

        particles[p][0][t] = particles[p][0][t-1] + a*np.cos(direction) # Mise à jour de la position en x
        particles[p][1][t] = particles[p][1][t-1] + a*np.sin(direction) # Mise à jour de la position en y

        if box:
            particles[p][0][t], particles[p][1][t] = bound_condition(particles[p][0][t], particles[p][1][t])
    return particles

# Mise en place des figure
def set_figure(figure_title : str, label_x : str, label_y : str, title : str, box : bool):
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(figure_title)

    if box:
        plt.hlines(L, -L, L, color = "black")
        plt.hlines(-L, -L, L, color = "black")
        plt.vlines(L, -L, L, color = "black")
        plt.vlines(-L, -L, L, color = "black")
    
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)
    return fig, ax


##############################################################################################################################
# Programme principal

fig1, ax1 = set_figure("Random Walk", "x", "y", "Évolution des différentes particules dans l’espace", box)
if video :
    fig2, ax2 = set_figure("Random Walk Video", "x", "y", "Évolution des différentes particules dans l’espace", box)
    artists = []

particles = np.zeros((n_particle, 2, n_step))   # Initialisation du tableau de particules

for t in range(1, n_step):
    print(f"Avancement des calculs : {round((t/n_step)*100, 2)} %")
    position_update(t, particles, n_particle)
    if video:
        frames = []
        time_text = ax2.text(0.075, 0.925, f"- Temps = {t} s", transform=ax2.transAxes, fontsize=10, verticalalignment='top')
        frames.append(time_text)
        for p in range(n_particle):
            x = particles[p][0][t]
            y = particles[p][1][t]
            point, = ax2.plot(x, y, marker = "o", color=f"C{p % 10}")
            frames.append(point)
        artists.append(frames)

for p in range(0, n_particle):
    ax1.plot(particles[p][0], particles[p][1])
print("Calculs Termines.")

if video :
    ani = animation.ArtistAnimation(fig=fig2, artists=artists, interval=50, blit=True)
    if save_video :
        ani.save('video/random_walk_video.mp4', writer='ffmpeg', fps=30)
        print("Video sauvegardee.")

plt.tight_layout()
plt.show()