import math
import collections
import matplotlib.pyplot as plt

def main():
    # Читання вхідних послідовностей з файлу
    original_sequences = []
    with open("sequence.txt", "r", encoding='utf-8') as file:
        for line in file:
            if '=' in line:
                seq = line.split('=')[1].strip()
                original_sequences.append(seq)

    # Обмеження до перших 10 символів кожної послідовності
    original_sequences = [seq[:10] for seq in original_sequences]

    results = []

    with open("results_AC_CH.txt", "w", encoding='utf-8') as file:
        for idx, sequence in enumerate(original_sequences, 1):
            file.write(f"{'/'*50}\n")
            file.write(f"Оригінальна послідовність {idx}: {sequence}\n")

            # Основні параметри послідовності
            sequence_length = len(sequence)
            unique_chars = list(set(sequence))
            sequence_alphabet_size = len(unique_chars)
            counts = collections.Counter(sequence)
            probability = {symbol: count / sequence_length for symbol, count in counts.items()}
            entropy = -sum(p * math.log2(p) for p in probability.values() if p > 0)

            file.write(f"Ентропія: {entropy:.4f}\n")

            # Арифметичне кодування
            file.write("\n_____Арифметичне кодування_____\n")
            encoded_data_ac, encoded_sequence_ac = encode_ac(unique_chars, probability, sequence_alphabet_size, sequence)
            bps_ac = len(encoded_sequence_ac) / sequence_length

            file.write(f"Дані закодованої AC послідовності: {encoded_data_ac}\n")
            file.write(f"Закодована AC послідовність: {encoded_sequence_ac}\n")
            file.write(f"Значення bps при кодуванні AC: {bps_ac:.1f}\n")

            decoded_sequence_ac = decode_ac(encoded_data_ac, sequence_length)
            file.write(f"Декодована AC послідовність: {decoded_sequence_ac}\n")

            # Кодування Хаффмана
            file.write("\n_____Кодування Хаффмана_____\n")
            encoded_data_hc, encoded_sequence_hc = encode_hc(unique_chars, probability, sequence)
            bps_hc = len(encoded_sequence_hc) / sequence_length

            file.write("Алфавіт\tКод символу\n")
            for symbol, code in encoded_data_hc[1]:
                file.write(f"{symbol}\t{code}\n")

            file.write(f"Дані закодованої HC послідовності: {encoded_data_hc}\n")
            file.write(f"Закодована HC послідовність: {encoded_sequence_hc}\n")
            file.write(f"Значення bps при кодуванні HC: {bps_hc:.1f}\n")

            decoded_sequence_hc = decode_hc(encoded_data_hc)
            file.write(f"Декодована HC послідовність: {decoded_sequence_hc}\n")

            results.append([round(entropy, 2), round(bps_ac, 1), round(bps_hc, 1)])

    # Побудова таблиці результатів
    plot_results(results)

def float_bin(point, size_cod):
    binary_code = ""
    for _ in range(size_cod):
        point *= 2
        if point > 1:
            binary_code += "1"
            point -= 1
        elif point < 1:
            binary_code += "0"
        else:
            binary_code += "1"
            break
    return binary_code

def encode_ac(uniq_chars, probabilitys, alphabet_size, sequence):
    alphabet = list(uniq_chars)
    probability = [probabilitys[symbol] for symbol in alphabet]

    unity = []
    probability_range = 0.0
    for i in range(alphabet_size):
        l = probability_range
        probability_range += probability[i]
        u = probability_range
        unity.append([alphabet[i], l, u])

    probability_low = 0.0
    probability_high = 1.0

    for i in range(len(sequence) - 1):
        for j in range(len(unity)):
            if sequence[i] == unity[j][0]:
                probability_low = unity[j][1]
                probability_high = unity[j][2]
                diff = probability_high - probability_low

                for k in range(len(unity)):
                    unity[k][1] = probability_low
                    unity[k][2] = probability[k] * diff + probability_low
                    probability_low = unity[k][2]
                break

    low = 0
    high = 0
    for i in range(len(unity)):
        if unity[i][0] == sequence[-1]:
            low = unity[i][1]
            high = unity[i][2]

    point = (low + high) / 2
    size_cod = math.ceil(math.log((1 / (high - low)), 2) + 1)
    bin_code = float_bin(point, size_cod)

    return [point, alphabet_size, alphabet, probability], bin_code

def decode_ac(encoded_data_ac, length_seq):
    point = encoded_data_ac[0]
    alphabet_size = encoded_data_ac[1]
    alphabet = encoded_data_ac[2]
    probability = encoded_data_ac[3]

    unity = []
    probability_range = 0.0
    for i in range(alphabet_size):
        l = probability_range
        probability_range += probability[i]
        u = probability_range
        unity.append([alphabet[i], l, u])

    decoded_sequence = ""
    for _ in range(length_seq):
        for j in range(len(unity)):
            if point > unity[j][1] and point < unity[j][2]:
                prob_low = unity[j][1]
                prob_high = unity[j][2]
                diff = prob_high - prob_low
                decoded_sequence += unity[j][0]

                for k in range(len(unity)):
                    unity[k][1] = prob_low
                    unity[k][2] = probability[k] * diff + prob_low
                    prob_low = unity[k][2]
                break

    return decoded_sequence

def encode_hc(uniq_chars, probabilitys, sequence):
    alphabet = list(uniq_chars)
    probability = [probabilitys[symbol] for symbol in alphabet]

    # Спеціальний випадок - всі символи однакові
    if len(set(probability)) == 1 and probability[0] == 1:
        symbol_code = []
        for i in range(len(alphabet)):
            code = "1" * i + "0"
            symbol_code.append([alphabet[i], code])
        encode = "".join([symbol_code[alphabet.index(c)][1] for c in sequence])
        return [encode, symbol_code], encode

    final = []
    for i in range(len(alphabet)):
        final.append([alphabet[i], probability[i]])
    final.sort(key=lambda x: x[1])

    tree = []
    while len(final) > 1:
        left = final.pop(0)
        right = final.pop(0)
        tot = left[1] + right[1]
        tree.append([left[0], right[0]])
        final.append([left[0] + right[0], tot])
        final.sort(key=lambda x: x[1])

    tree.reverse()

    symbol_code = []
    alphabet.sort()
    for char in alphabet:
        code = ""
        for node in tree:
            if char in node[0]:
                code += "0"
                if char == node[0]:
                    break
            else:
                code += "1"
                if char == node[1]:
                    break
        symbol_code.append([char, code])

    encode = ""
    for c in sequence:
        for symbol, code in symbol_code:
            if c == symbol:
                encode += code
                break

    return [encode, symbol_code], encode

def decode_hc(encoded_sequence):
    encode = list(encoded_sequence[0])
    symbol_code = encoded_sequence[1]

    sequence = ""
    current_code = ""

    for bit in encode:
        current_code += bit
        for symbol, code in symbol_code:
            if current_code == code:
                sequence += symbol
                current_code = ""
                break

    return sequence

def plot_results(results):
    N = len(results)
    fig, ax = plt.subplots(figsize=(14/1.54, N/1.54))

    headers = ['Ентропія', 'bps AC', 'bps CH']
    row = [f'Послідовність {i+1}' for i in range(N)]

    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row,
                     loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)

    plt.savefig("Результати стиснення методами АС та СН.png", bbox_inches='tight', dpi=300)

if __name__ == "__main__":
    main()