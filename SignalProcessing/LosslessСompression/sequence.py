import random
import collections
import math
import string
import matplotlib.pyplot as plt

# Константи
N_SEQUENCE = 100
STUDENT_NUMBER = 5  # Порядковий номер
LAST_NAME = "Dovhiy"
GROUP_NUMBER = "529"

def generate_sequence_1():
    """Генерація послідовності 1"""
    list1 = ['1'] * STUDENT_NUMBER
    list0 = ['0'] * (N_SEQUENCE - STUDENT_NUMBER)
    combined = list1 + list0
    random.shuffle(combined)
    return ''.join(combined)

def generate_sequence_2():
    """Генерація послідовності 2"""
    letters = list(LAST_NAME)
    zeros = ['0'] * (N_SEQUENCE - len(letters))
    return ''.join(letters + zeros)

def generate_sequence_3():
    """Генерація послідовності 3"""
    letters = list(LAST_NAME)
    zeros = ['0'] * (N_SEQUENCE - len(letters))
    combined = letters + zeros
    random.shuffle(combined)
    return ''.join(combined)

def generate_sequence_4():
    """Генерація послідовності 4"""
    letters = list(LAST_NAME) + list(GROUP_NUMBER)
    n_letters = len(letters)
    n_repeats = N_SEQUENCE // n_letters
    remainder = N_SEQUENCE % n_letters

    sequence = letters * n_repeats + letters[:remainder]
    return ''.join(sequence)

def generate_sequence_5():
    """Генерація послідовності 5"""
    elements = list(LAST_NAME[:2]) + list(GROUP_NUMBER)
    sequence = random.choices(elements, k=N_SEQUENCE)
    return ''.join(sequence)

def generate_sequence_6():
    """Генерація послідовності 6"""
    letters = list(LAST_NAME[:2])
    digits = list(GROUP_NUMBER)

    n_letters = int(0.7 * N_SEQUENCE)
    n_digits = N_SEQUENCE - n_letters

    sequence = random.choices(letters, k=n_letters) + random.choices(digits, k=n_digits)
    random.shuffle(sequence)
    return ''.join(sequence)

def generate_sequence_7():
    """Генерація послідовності 7"""
    elements = string.ascii_lowercase + string.digits
    sequence = random.choices(elements, k=N_SEQUENCE)
    return ''.join(sequence)

def generate_sequence_8():
    """Генерація послідовності 8"""
    return '1' * N_SEQUENCE

def calculate_sequence_stats(sequence):
    """Розрахунок статистики для послідовності"""
    # Розмір алфавіту
    unique_chars = set(sequence)
    alphabet_size = len(unique_chars)

    # Розмір послідовності в байтах
    sequence_size_bytes = len(sequence)

    # Ймовірності символів
    counts = collections.Counter(sequence)
    probability = {symbol: count / N_SEQUENCE for symbol, count in counts.items()}

    # Середня ймовірність
    mean_probability = sum(probability.values()) / len(probability)

    # Тип розподілу ймовірностей
    equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
    uniformity = "рівна" if equal else "нерівна"

    # Ентропія
    entropy = -sum(p * math.log2(p) for p in probability.values() if p > 0)

    # Надмірність
    if alphabet_size > 1:
        source_excess = 1 - entropy / math.log2(alphabet_size)
    else:
        source_excess = 1

    return {
        'sequence': sequence,
        'alphabet_size': alphabet_size,
        'size_bytes': sequence_size_bytes,
        'probability': probability,
        'mean_probability': mean_probability,
        'uniformity': uniformity,
        'entropy': entropy,
        'source_excess': source_excess
    }

def save_results_to_file(stats, filename="results_sequence.txt"):
    """Збереження результатів у файл"""
    with open(filename, "w", encoding="utf-8") as file:
        for i, stat in enumerate(stats, 1):
            file.write(f"Послідовність {i}: {stat['sequence']}\n")
            file.write(f"Розмір послідовності: {stat['size_bytes']} byte\n")
            file.write(f"Розмір алфавіту: {stat['alphabet_size']}\n")

            prob_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in stat['probability'].items()])
            file.write(f"Ймовірності появи символів: {prob_str}\n")
            file.write(f"Середнє арифметичне ймовірностей: {stat['mean_probability']:.2f}\n")
            file.write(f"Ймовірність розподілу символів: {stat['uniformity']}\n")
            file.write(f"Ентропія: {stat['entropy']:.4f}\n")
            file.write(f"Надмірність джерела: {stat['source_excess']:.2f}\n\n")

def save_sequences_to_file(sequences, filename="sequence.txt"):
    """Збереження послідовностей у файл"""
    with open(filename, "w", encoding="utf-8") as file:
        for i, seq in enumerate(sequences, 1):
            file.write(f"original_sequence_{i}={seq}\n")

def create_results_table(stats):
    """Створення таблиці з результатами"""
    results = []
    for stat in stats:
        results.append([
            stat['alphabet_size'],
            round(stat['entropy'], 2),
            round(stat['source_excess'], 2),
            stat['uniformity']
        ])

    return results

def plot_table(results):
    """Візуалізація результатів у вигляді таблиці"""
    N = len(results)
    fig, ax = plt.subplots(figsize=(14/1.54, N/1.54))
    ax.axis('off')

    headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
    rows = [f'Послідовність {i+1}' for i in range(N)]

    table = ax.table(
        cellText=results,
        colLabels=headers,
        rowLabels=rows,
        loc='center',
        cellLoc='center'
    )

    table.set_fontsize(14)
    table.scale(0.8, 2)
    plt.savefig('Характеристики сформованих послідовностей.png', bbox_inches='tight')
    plt.close()

def main():
    # Генерація послідовностей
    sequences = [
        generate_sequence_1(),
        generate_sequence_2(),
        generate_sequence_3(),
        generate_sequence_4(),
        generate_sequence_5(),
        generate_sequence_6(),
        generate_sequence_7(),
        generate_sequence_8()
    ]

    # Розрахунок статистики для кожної послідовності
    stats = [calculate_sequence_stats(seq) for seq in sequences]

    # Збереження результатів
    save_results_to_file(stats)
    save_sequences_to_file(sequences)

    # Створення таблиці результатів
    results_table = create_results_table(stats)
    plot_table(results_table)

if __name__ == "__main__":
    main()