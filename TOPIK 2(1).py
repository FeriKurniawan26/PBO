def calculate_average(numbers):
    try:
        # Memastikan input adalah list
        if not isinstance(numbers, list):
            raise ValueError("Input harus berupa list.")
        
        # Memastikan semua elemen dalam list adalah angka
        for num in numbers:
            if not isinstance(num, (int, float)):
                raise ValueError("Semua elemen dalam list harus berupa angka.")
        
        total = sum(numbers)
        average = total / len(numbers)
        return average
    
    except ValueError as e:
        return f"Error: {e}"

# Contoh penggunaan
result = calculate_average([5, 5, 7, 8])  # input yang benar adalah list
print(result)

# Contoh input yang salah
result = calculate_average("5, 5, 7, 8")  # input berupa string
print(result)

result = calculate_average([5, 5, '7', 8])  # input dengan elemen string
print(result)

result = calculate_average([5, 5, 7, 8, None])  # input dengan elemen None
print(result)