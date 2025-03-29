import ast
import collections
import math
import matplotlib.pyplot as plt

def read_sequences(filename="sequence.txt"):
    """Зчитування послідовностей з файлу"""
    with open(filename, "r", encoding='utf-8') as file:
        sequences = []
        for line in file:
            line = line.strip()
            if '=' in line:
                seq = line.split('=', 1)[1].strip('"\'')
                sequences.append(seq)
    return sequences

def calculate_entropy(sequence):
    """Розрахунок ентропії послідовності"""
    counts = collections.Counter(sequence)
    probability = {symbol: count / len(sequence) for symbol, count in counts.items()}
    entropy = -sum(p * math.log2(p) for p in probability.values() if p > 0)
    return entropy

def encode_rle(sequence, max_count=1000):
    """Кодування RLE з обмеженням максимальної кількості"""
    if not sequence:
        return ""

    result = []
    count = 1

    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            count += 1
            if count > max_count:
                result.append(f"{max_count}{sequence[i-1]}")
                count = 1
        else:
            result.append(f"{count}{sequence[i-1]}")
            count = 1

    result.append(f"{count}{sequence[-1]}")
    return "".join(result)

def decode_rle(encoded_sequence):
    """Декодування RLE з обробкою великих чисел"""
    decoded = []
    i = 0
    while i < len(encoded_sequence):
        count_str = ""
        while i < len(encoded_sequence) and encoded_sequence[i].isdigit():
            count_str += encoded_sequence[i]
            i += 1

        if i >= len(encoded_sequence):
            break

        symbol = encoded_sequence[i]
        count = int(count_str) if count_str else 1

        # Process in chunks to avoid memory issues
        chunk_size = 1000000  # 1 million characters at a time
        full_chunks = count // chunk_size
        remainder = count % chunk_size

        for _ in range(full_chunks):
            decoded.append(symbol * chunk_size)
        if remainder > 0:
            decoded.append(symbol * remainder)

        i += 1

    return "".join(decoded)

def encode_lzw(sequence):
    """Кодування LZW"""
    dictionary = {chr(i): i for i in range(65536)}
    next_code = 65536
    result = []
    current = ""

    for symbol in sequence:
        new_str = current + symbol
        if new_str in dictionary:
            current = new_str
        else:
            result.append(dictionary[current])
            dictionary[new_str] = next_code
            next_code += 1
            current = symbol

    if current:
        result.append(dictionary[current])

    return result

def decode_lzw(encoded_sequence):
    """Декодування LZW"""
    dictionary = {i: chr(i) for i in range(65536)}
    next_code = 65536
    result = []
    previous = None

    for code in encoded_sequence:
        if code in dictionary:
            current = dictionary[code]
        elif code == next_code:
            current = previous + previous[0]
        else:
            raise ValueError("Невірний код")

        result.append(current)

        if previous is not None:
            dictionary[next_code] = previous + current[0]
            next_code += 1

        previous = current

    return "".join(result)

def save_results(filename, original_seq, encoded_rle, decoded_rle, encoded_lzw, decoded_lzw,
                 entropy, cr_rle, cr_lzw, seq_num):
    """Компактне збереження результатів"""
    with open(filename, "a", encoding='utf-8') as file:
        file.write(f"\n=== Послідовність {seq_num} ===\n")
        file.write(f"Ентропія: {entropy:.4f}\n")

        # RLE results
        rle_ratio = f"{len(original_seq)}->{len(encoded_rle)}" if cr_rle != "-" else "N/A"
        file.write(f"RLE: коеф. {cr_rle} ({rle_ratio}) | ")

        # LZW results
        lzw_size = sum(math.ceil(math.log2(code+1)) if code < 65536 else 17 for code in encoded_lzw)
        lzw_ratio = f"{len(original_seq)*16}b->{lzw_size}b"
        file.write(f"LZW: коеф. {cr_lzw} ({lzw_ratio})\n")

        # Validation
        valid_rle = "OK" if decoded_rle == original_seq else "ERROR"
        valid_lzw = "OK" if decoded_lzw == original_seq else "ERROR"
        file.write(f"Перевірка: RLE {valid_rle}, LZW {valid_lzw}\n")

def create_results_table(results, filename="Результати стиснення.png"):
    """Створення оптимізованої таблиці"""
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    ax.axis('off')

    col_labels = ['Послідовність', 'Ентропія', 'RLE (КС)', 'LZW (КС)', 'Валідність']
    cell_text = []

    for i, res in enumerate(results, 1):
        entropy, cr_rle, cr_lzw, valid = res
        cell_text.append([
            f"{i}",
            f"{entropy:.2f}",
            f"{cr_rle}",
            f"{cr_lzw}",
            valid
        ])

    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        loc='center',
        cellLoc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    sequences = read_sequences()
    table_results = []

    with open("results_rle_lzw.txt", "w", encoding='utf-8') as file:
        file.write("=== Результати стиснення ===\n")
        file.write("Формат: коефіцієнт стиснення (розмір до->після)\n")
        file.write("="*50 + "\n")

    for i, seq in enumerate(sequences, 1):
        try:
            entropy = calculate_entropy(seq)

            # RLE encoding/decoding
            encoded_rle = encode_rle(seq)
            decoded_rle = decode_rle(encoded_rle)
            cr_rle = round((len(seq)*16)/(len(encoded_rle)*16), 2) if len(encoded_rle)*16 < len(seq)*16 else "-"

            # LZW encoding/decoding
            encoded_lzw = encode_lzw(seq)
            decoded_lzw = decode_lzw(encoded_lzw)
            lzw_size = sum(math.ceil(math.log2(code+1)) if code < 65536 else 17 for code in encoded_lzw)
            cr_lzw = round((len(seq)*16)/lzw_size, 2)

            # Save results
            save_results("results_rle_lzw.txt", seq, encoded_rle, decoded_rle,
                         encoded_lzw, decoded_lzw, entropy, cr_rle, cr_lzw, i)

            # Prepare table data
            valid = "OK" if decoded_rle == seq and decoded_lzw == seq else "ERROR"
            table_results.append((entropy, cr_rle, cr_lzw, valid))

        except Exception as e:
            table_results.append((0, "-", "-", "ERROR"))

    create_results_table(table_results)

if __name__ == "__main__":
    main()