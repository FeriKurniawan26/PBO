class Rekening:
    def __init__(self, no_rekening, nama_pemilik, saldo=0):
        self.no_rekening = no_rekening
        self.nama_pemilik = nama_pemilik
        self.saldo = saldo

    def setor(self, jumlah): 
        self.saldo += jumlah
        print(f"Setor {jumlah} berhasil. Saldo: {self.saldo}")

    def tarik(self, jumlah): 
        if jumlah <= self.saldo: 
            self.saldo -= jumlah
            print(f"Tarik {jumlah} berhasil. Saldo: {self.saldo}")
        else: 
            print("Saldo tidak mencukupi.")

    def cek_saldo(self): 
        print(f"Saldo saat ini: {self.saldo}")

    def info_rekening(self):
        print(f"Rekening: {self.no_rekening} | Pemilik: {self.nama_pemilik} | Saldo: {self.saldo}")

# Membuat objek dan pemanggilan metode
rekening1 = Rekening("123456789", "Nipsu", 1000)
rekening1.info_rekening()
rekening1.setor(2000)
rekening1.tarik(1000)
rekening1.cek_saldo()