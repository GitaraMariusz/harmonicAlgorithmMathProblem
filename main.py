import random
import math

# --- Funkcja Celu (Fitness) ---
def calculate_fitness(harmony, numbers, target_average):
    """
    Oblicza jakość (fitness) danej harmonii (permutacji liczb).
    Celem jest minimalizacja sumy absolutnych różnic między sumą każdej pary
    a docelową średnią sumą pary.
    Niższy wynik oznacza lepsze dopasowanie.
    """
    if not harmony:
        return float('inf') # Najgorszy możliwy wynik dla pustej harmonii

    total_deviation = 0
    num_pairs = len(numbers) // 2

    for i in range(num_pairs):
        # Sprawdzenie, czy indeksy są w zakresie (choć przy permutacji nie powinno to być problemem)
        idx1 = 2 * i
        idx2 = 2 * i + 1
        if idx1 < len(harmony) and idx2 < len(harmony):
            pair_sum = harmony[idx1] + harmony[idx2]
            total_deviation += abs(pair_sum - target_average)
        else:
             # Kara za niekompletną harmonię (teoretycznie nie powinno wystąpić przy poprawnej implementacji)
            total_deviation += float('inf') / num_pairs

    return total_deviation

# --- Operatory dla Algorytmu Harmonicznego (dla problemu permutacyjnego) ---

def generate_random_harmony(numbers):
    """Generuje losową permutację liczb jako nową harmonię."""
    harmony = numbers[:] # Stwórz kopię
    random.shuffle(harmony)
    return harmony

def apply_pitch_adjustment(harmony):
    """
    Stosuje "Pitch Adjustment" odpowiedni dla permutacji - zamiana miejscami dwóch losowych elementów.
    Odpowiednik modyfikacji wartości w ciągłym HS.
    """
    if len(harmony) < 2:
        return harmony # Nie można zamienić w zbyt krótkiej liście

    idx1, idx2 = random.sample(range(len(harmony)), 2) # Wybierz dwa RÓŻNE indeksy
    harmony[idx1], harmony[idx2] = harmony[idx2], harmony[idx1]
    return harmony

# --- Główna funkcja Algorytmu Harmonicznego ---
def harmony_search_pairing(numbers, hms, hmcr, par, ni):
    """
    Implementuje algorytm Harmony Search do problemu parowania liczb.

    Args:
        numbers (list): Lista liczb do sparowania (musi mieć parzystą długość).
        hms (int): Rozmiar pamięci harmonii (Harmony Memory Size).
        hmcr (float): Współczynnik uwzględniania pamięci harmonii (Harmony Memory Considering Rate, 0 <= hmcr <= 1).
        par (float): Współczynnik dostosowania tonacji (Pitch Adjusting Rate, 0 <= par <= 1).
        ni (int): Liczba improwizacji (iteracji).

    Returns:
        tuple: (best_harmony, best_fitness) - najlepsza znaleziona permutacja i jej wynik fitness.
               Lub (None, float('inf')) jeśli dane wejściowe są nieprawidłowe.
    """
    n = len(numbers)
    if n % 2 != 0:
        print("Błąd: Liczba elementów musi być parzysta.")
        return None, float('inf')
    if n == 0:
        print("Błąd: Lista liczb jest pusta.")
        return [], 0 # Zwracamy pustą listę i zerowy koszt dla pustego wejścia

    total_sum = sum(numbers)
    num_pairs = n // 2
    target_average = total_sum / num_pairs
    print(f"Liczba elementów: {n}, Liczba par: {num_pairs}, Suma całkowita: {total_sum}, Średnia suma pary: {target_average:.2f}")

    # 1. Inicjalizacja Pamięci Harmonii (HM)
    harmony_memory = []
    for _ in range(hms):
        harmony = generate_random_harmony(numbers)
        fitness = calculate_fitness(harmony, numbers, target_average)
        harmony_memory.append({'harmony': harmony, 'fitness': fitness})

    # Sortowanie HM - najlepsze (najniższy fitness) na początku
    harmony_memory.sort(key=lambda x: x['fitness'])

    print(f"Początkowy najlepszy fitness: {harmony_memory[0]['fitness']:.4f}")

    # 2. Główna pętla improwizacji
    for iteration in range(ni):
        new_harmony_elements = [] # Będziemy budować nową harmonię

        # Decyzja o sposobie generowania nowej harmonii na podstawie HMCR
        rand_hmcr = random.random()

        if rand_hmcr < hmcr:
            # Uwzględnij pamięć harmonii
            # Wybierz losową harmonię bazową z HM
            base_harmony_idx = random.randint(0, hms - 1)
            base_harmony = harmony_memory[base_harmony_idx]['harmony']
            new_harmony = base_harmony[:] # Stwórz kopię

            # Zastosuj Pitch Adjustment z prawdopodobieństwem PAR
            rand_par = random.random()
            if rand_par < par:
                new_harmony = apply_pitch_adjustment(new_harmony)

        else:
            # Generuj całkowicie losową harmonię (Improwizacja losowa)
            new_harmony = generate_random_harmony(numbers)

        # 3. Oblicz fitness nowej harmonii
        new_fitness = calculate_fitness(new_harmony, numbers, target_average)

        # 4. Aktualizacja Pamięci Harmonii
        # Znajdź najgorszą harmonię w HM (jest na końcu posortowanej listy)
        worst_fitness = harmony_memory[-1]['fitness']

        if new_fitness < worst_fitness:
            # Zastąp najgorszą harmonię nową, lepszą harmonią
            harmony_memory[-1] = {'harmony': new_harmony, 'fitness': new_fitness}
            # Ponownie posortuj, aby utrzymać porządek
            harmony_memory.sort(key=lambda x: x['fitness'])

        # Opcjonalnie: Wyświetlanie postępu co pewną liczbę iteracji
        if (iteration + 1) % (ni // 10) == 0:
             print(f"Iteracja {iteration + 1}/{ni}, Najlepszy fitness: {harmony_memory[0]['fitness']:.4f}")


    # 5. Zwróć najlepszą harmonię znalezioną w HM
    best_solution = harmony_memory[0]
    print(f"\nZakończono po {ni} iteracjach.")
    print(f"Najlepszy znaleziony fitness: {best_solution['fitness']:.4f}")

    # Formatowanie wyniku dla lepszej czytelności
    best_pairs = []
    final_harmony = best_solution['harmony']
    for i in range(num_pairs):
        idx1 = 2 * i
        idx2 = 2 * i + 1
        pair = (final_harmony[idx1], final_harmony[idx2])
        pair_sum = sum(pair)
        diff = abs(pair_sum - target_average)
        best_pairs.append({'pair': pair, 'sum': pair_sum, 'diff': diff})

    print(f"Średnia suma pary docelowa: {target_average:.2f}")
    print("Najlepsze znalezione pary:")
    for p_info in best_pairs:
        print(f"  Para: {p_info['pair']}, Suma: {p_info['sum']}, Różnica od średniej: {p_info['diff']:.2f}")


    return best_solution['harmony'], best_solution['fitness']

# --- Przykład użycia ---
if __name__ == "__main__":
    # Przykładowy zbiór liczb
    # numbers_to_pair = [1, 9, 2, 8, 3, 7, 4, 6, 10, 5, 11, 12]
    # numbers_to_pair = [1, 2, 3, 10, 11, 12, 20, 21, 22, 30, 31, 32]
    numbers_to_pair = random.sample(range(1, 1001), 200) # Większy, losowy zestaw

    # Parametry algorytmu Harmony Search
    HMS = 20      # Rozmiar pamięci harmonii
    HMCR = 0.9    # Prawdopodobieństwo wybrania z pamięci
    PAR = 0.3     # Prawdopodobieństwo modyfikacji (zamiany miejsc)
    NI = 50000     # Liczba iteracji

    print("Dane wejściowe:", numbers_to_pair)
    print("\nUruchamianie Algorytmu Harmonicznego...")

    best_harmony, best_fitness = harmony_search_pairing(numbers_to_pair, HMS, HMCR, PAR, NI)

    # Wyświetlenie ostatecznego wyniku (już w funkcji)
    if best_harmony:
        print("\nOstateczny wynik:")
        print("Najlepsza permutacja (kolejność parowania):", best_harmony)
        print(f"Najlepszy fitness (minimalna suma odchyleń): {best_fitness:.4f}")