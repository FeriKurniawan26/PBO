def convert_to_int(string):
    try:
        result = int(string)
        return result
    except ValueError:
        return None  # Mengembalikan None jika konversi gagal

# Meminta input dari pengguna
umur = input('Masukkan umur kamu: ')  # inputan yang benar adalah angka

# Mengonversi umur dan menambahkan 5 tahun
umur5tahunlagi = convert_to_int(umur)

if umur5tahunlagi is not None:
    print(f"Umur kamu 5 tahun lagi adalah {umur5tahunlagi + 5}")
else:
    print("Error: Input harus berupa angka.")