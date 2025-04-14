import random
import time
import tracemalloc
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Algorithmes de tri ---
def tri_insertion(arr):
    for i in range(1, len(arr)):
        cle = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > cle:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = cle

def tri_selection(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def tri_bulle(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def tri_fusion(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        tri_fusion(L)
        tri_fusion(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def tri_rapide(arr):
    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    quick_sort(arr, 0, len(arr) - 1)

def tri_par_tas(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

def tri_a_peigne(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1

# [Même que dans ton code original – inchangé]

# --- Dictionnaire des algos ---
algos = {
    "Tri à bulles": tri_bulle,
    "Tri par insertion": tri_insertion,
    "Tri par sélection": tri_selection,
    "Tri fusion": tri_fusion,
    "Tri rapide": tri_rapide,
    "Tri par tas": tri_par_tas,
    "Tri à peigne": tri_a_peigne
}

# --- Fonction de mesure ---
def mesurer_performance(algo, data):
    liste_test = data.copy()
    tracemalloc.start()
    debut = time.perf_counter()
    algo(liste_test)
    fin = time.perf_counter()
    memoire, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return fin - debut, memoire / 1024  # en Ko

# --- Gérer la taille de liste ---
def generer_liste():
    taille = int(combo_taille.get())
    return [random.randint(1, 1000) for _ in range(taille)]

# --- Interface Graphique ---
def afficher_comparaison():
    liste = generer_liste()
    performances = {}

    for nom, algo in algos.items():
        temps, memoire = mesurer_performance(algo, liste)
        performances[nom] = (temps, memoire)

    noms = list(performances.keys())
    temps = [performances[n][0] for n in noms]
    memoire = [performances[n][1] for n in noms]

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    bars1 = ax1.bar(noms, temps, color='skyblue', label='Temps (s)')
    bars2 = ax2.bar(noms, memoire, color='lightgreen', alpha=0.6, label='Mémoire (Ko)')

    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height + 0.002, f'{height:.4f}', ha='center', va='bottom', fontsize=8)

    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height:.1f}', ha='center', va='bottom', fontsize=8)

    ax1.set_ylabel('Temps (secondes)')
    ax2.set_ylabel('Mémoire (Ko)')
    ax1.set_title(f"Comparaison des algorithmes - Taille {len(liste)}")

    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)

def afficher_algo_selectionne():
    nom_algo = combo_algo.get()
    if nom_algo not in algos:
        return

    liste = generer_liste()
    algo = algos[nom_algo]
    temps, memoire = mesurer_performance(algo, liste)

    fig, ax = plt.subplots(figsize=(4, 5))
    bars = ax.bar(["Temps", "Mémoire"], [temps, memoire], color=['dodgerblue', 'seagreen'])

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.01, f'{height:.4f}' if bar.get_x() < 1 else f'{height:.1f}', ha='center', va='bottom', fontsize=8)

    ax.set_title(f"Performance : {nom_algo} (Taille {len(liste)})")
    ax.set_ylabel("Valeur (s / Ko)")

    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)

# --- Application Tkinter ---
app = tk.Tk()
app.title("Comparaison d'Algorithmes de Tri")
app.geometry("1000x750")

frame_controls = tk.Frame(app)
frame_controls.pack(pady=10)

btn_comparer = tk.Button(frame_controls, text="Comparer tous les algorithmes", command=afficher_comparaison)
btn_comparer.grid(row=0, column=0, padx=10)

combo_algo = ttk.Combobox(frame_controls, values=list(algos.keys()), width=25)
combo_algo.grid(row=0, column=1, padx=10)
combo_algo.set("Choisir un algorithme")

btn_afficher_un = tk.Button(frame_controls, text="Afficher sélection", command=afficher_algo_selectionne)
btn_afficher_un.grid(row=0, column=2, padx=10)

label_taille = tk.Label(frame_controls, text="Taille de la liste :")
label_taille.grid(row=0, column=3, padx=10)

combo_taille = ttk.Combobox(frame_controls, values=["10", "100", "500", "1000", "5000", "10000"], width=10)
combo_taille.grid(row=0, column=4, padx=10)
combo_taille.set("100")  # Valeur par défaut

frame_graph = tk.Frame(app)
frame_graph.pack(fill=tk.BOTH, expand=True)

app.mainloop()
