import random
import time
import plotly.graph_objects as go

# Fonctions de tri
def tri_selection(ma_liste):
    for i in range(len(ma_liste)):
        plus_petit = i
        for j in range(i + 1, len(ma_liste)):
            if ma_liste[j] < ma_liste[plus_petit]:
                plus_petit = j
        ma_liste[i], ma_liste[plus_petit] = ma_liste[plus_petit], ma_liste[i]

def tri_bulles(ma_liste):
    for i in range(len(ma_liste)):
        for j in range(0, len(ma_liste) - i - 1):
            if ma_liste[j] > ma_liste[j + 1]:
                ma_liste[j], ma_liste[j + 1] = ma_liste[j + 1], ma_liste[j]

def tri_insertion(ma_liste):
    for i in range(1, len(ma_liste)):
        valeur = ma_liste[i]
        j = i - 1
        while j >= 0 and valeur < ma_liste[j]:
            ma_liste[j + 1] = ma_liste[j]
            j -= 1
        ma_liste[j + 1] = valeur

def tri_fusion(ma_liste):
    if len(ma_liste) > 1:
        mid = len(ma_liste) // 2
        L = ma_liste[:mid]
        R = ma_liste[mid:]
        tri_fusion(L)
        tri_fusion(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                ma_liste[k] = L[i]
                i += 1
            else:
                ma_liste[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            ma_liste[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            ma_liste[k] = R[j]
            j += 1
            k += 1

def tri_rapide(ma_liste):
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i+1

    def quicksort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort(arr, low, pi-1)
            quicksort(arr, pi+1, high)

    quicksort(ma_liste, 0, len(ma_liste) - 1)

def tri_tas(ma_liste):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(ma_liste)
    for i in range(n // 2 - 1, -1, -1):
        heapify(ma_liste, n, i)
    for i in range(n-1, 0, -1):
        ma_liste[i], ma_liste[0] = ma_liste[0], ma_liste[i]
        heapify(ma_liste, i, 0)

def tri_peigne(ma_liste):
    gap = len(ma_liste)
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < len(ma_liste):
            if ma_liste[i] > ma_liste[i + gap]:
                ma_liste[i], ma_liste[i + gap] = ma_liste[i + gap], ma_liste[i]
                sorted = False
            i += 1

# Génère une liste aléatoire
def liste_aleatoire(taille):
    return [random.randint(0, 100) for _ in range(taille)]

# Teste les algorithmes et mesure les temps
def main():
    taille = 100
    liste_depart = liste_aleatoire(taille)

    tris = [
        ("Sélection", tri_selection),
        ("Bulles", tri_bulles),
        ("Insertion", tri_insertion),
        ("Fusion", tri_fusion),
        ("Rapide", tri_rapide),
        ("Tas", tri_tas),
        ("Peigne", tri_peigne),
    ]

    resultats = []
    for nom, algo in tris:
        copie = liste_depart.copy()
        debut = time.time()
        algo(copie)
        fin = time.time()
        resultats.append((nom, fin - debut))

    return resultats

# Affiche l'animation avec Plotly
def afficher_graphique_avec_animation(resultats):
    noms = [nom for nom, _ in resultats]
    valeurs = [t for _, t in resultats]
    max_val = max(valeurs)
    steps = 50  # nombre d'étapes d'animation
    frames = []

    # Génère des frames pour simuler les barres qui montent
    for step in range(steps + 1):
        y = [(v / max_val) * step / steps * max_val for v in valeurs]
        frames.append(go.Frame(data=[go.Bar(x=noms, y=y)]))

    fig = go.Figure(
        data=[go.Bar(x=noms, y=[0]*len(noms), marker_color="skyblue")],
        layout=go.Layout(
            title="Comparaison des temps d'exécution des algorithmes de tri",
            xaxis_title="Algorithme",
            yaxis_title="Temps (secondes)",
            yaxis=dict(range=[0, max(valeurs) * 1.2]),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                buttons=[dict(label="Lancer animation",
                              method="animate",
                              args=[None, {"frame": {"duration": 100, "redraw": True},
                                           "fromcurrent": True}])]
            )]
        ),
        frames=frames
    )

    fig.show()

# Lancer tout ça
if __name__ == "__main__":
    resultats = main()
    afficher_graphique_avec_animation(resultats)
