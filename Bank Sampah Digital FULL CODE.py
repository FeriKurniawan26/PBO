from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QTabWidget, QGroupBox, QListWidget, QListWidgetItem,
    QGridLayout, QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
import json
import os
import sys

class BankSampahApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank Sampah Digital - Konohagakure no Sato")
        self.setMinimumSize(QSize(800, 600))
        self.database_file = "database.json"
        self.current_user = None
        self.fullscreen = False

        self.konversi = {
            'kertas': 15,
            'kaca': 25,
            'plastik': 35,
            'logam': 40,
            'elektronik': 50
        }

        self.penukaran = {
            'pulsa': {'poin': 50, 'hadiah': 'Pulsa 20.000'},
            'uang50': {'poin': 125, 'hadiah': 'Uang Rp50.000'},
            'voucher': {'poin': 150, 'hadiah': 'Peralatan / Perabotan Rumah Tangga'},
            'hukum': {'poin': 200, 'hadiah': 'Hukum Di Indonesia'}
        }

        self.users = self.load_database()
        self.initUI()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def load_database(self):
        if os.path.exists(self.database_file):
            try:
                with open(self.database_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_database(self):
        with open(self.database_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # User Selection
        user_layout = QHBoxLayout()
        self.user_combo = QComboBox()
        self.user_combo.addItems(self.users.keys())
        self.user_combo.currentTextChanged.connect(self.select_user)
        
        self.new_user_input = QLineEdit(placeholderText="Nama pengguna baru...")
        btn_add_user = QPushButton("Tambah Pengguna", clicked=self.add_user)
        
        user_layout.addWidget(QLabel("Pilih Pengguna:"))
        user_layout.addWidget(self.user_combo)
        user_layout.addWidget(self.new_user_input)
        user_layout.addWidget(btn_add_user)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("QTabBar::tab { height: 30px; min-width: 100px; }")
        
        # Create Tabs
        tabs.addTab(self.create_deposit_tab(), "Setor Sampah")
        tabs.addTab(self.create_exchange_tab(), "Tukar Poin")
        tabs.addTab(self.create_history_tab(), "Riwayat")
        tabs.addTab(self.create_users_tab(), "Daftar Pengguna")
        
        # Status
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #2c3e50; padding: 10px;")
        
        main_layout.addLayout(user_layout)
        main_layout.addWidget(tabs, 1)
        main_layout.addWidget(self.status_label)
        self.setLayout(main_layout)

    def create_deposit_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Input Group
        group = QGroupBox("Form Setor Sampah")
        group.setStyleSheet("QGroupBox { font-weight: bold; color: #2c3e50; }")
        form_layout = QVBoxLayout()
        
        # Input fields
        self.nama_input = QLineEdit(placeholderText="Masukkan nama...")
        self.jenis_combo = QComboBox()
        self.jenis_combo.addItems([jenis.capitalize() for jenis in self.konversi.keys()])
        self.berat_input = QLineEdit(placeholderText="Berat (kg)...")
        
        # Styling
        input_style = """
            QLineEdit, QComboBox {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin: 5px;
            }
            QLineEdit:focus, QComboBox:hover { border-color: #3498db; }
        """
        self.nama_input.setStyleSheet(input_style)
        self.berat_input.setStyleSheet(input_style)
        self.jenis_combo.setStyleSheet(input_style)
        
        form_layout.addWidget(QLabel("Nama:"))
        form_layout.addWidget(self.nama_input)
        form_layout.addWidget(QLabel("Jenis Sampah:"))
        form_layout.addWidget(self.jenis_combo)
        form_layout.addWidget(QLabel("Berat:"))
        form_layout.addWidget(self.berat_input)
        group.setLayout(form_layout)
        
        # Conversion Grid
        conversion_group = QGroupBox("Nilai Konversi")
        grid = QGridLayout()
        materials = [
            ('kertas', 15, "#8b8d83"),
            ('kaca', 25, '#2980b9'),
            ('plastik', 35, "#0fc91f"),
            ('logam', 40, "#d6c914"),
            ('Elektronik', 50, "#f10f0f")
        ]
        for i, (name, point, color) in enumerate(materials):
            card = QLabel(f"""
                <div style='background:{color}; padding:15px; border-radius:8px; color:white;' >
                    <b>{name}</b><br>{point} poin/kg
                </div>
            """)
            card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(card, i//2, i%2)
        conversion_group.setLayout(grid)
        
        # Deposit Button
        btn_setor = QPushButton("🗑️ Setor Sekarang", clicked=self.setor_sampah)
        btn_setor.setStyleSheet("""
            QPushButton {
                background: #2ecc71; color: white; padding: 15px;
                border-radius: 8px; font-size: 16px; border: none;
                margin: 10px;
            }
            QPushButton:hover { background: #27ae60; }
        """)
        
        layout.addWidget(group)
        layout.addWidget(conversion_group)
        layout.addWidget(btn_setor, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(1)
        tab.setLayout(layout)
        return tab

    def create_exchange_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.poin_label = QLabel()
        self.poin_label.setStyleSheet("font-size: 18px; color: #e67e22; font-weight: bold;")
        
        group = QGroupBox("Pilihan Penukaran Poin")
        vbox = QVBoxLayout()
        
        # Warna background untuk tiap jenis penukaran
        warna_penukaran = {
            'pulsa': "#a0a0a0",      # abu
            'uang50': "#ccd81e",       # kuning
            'voucher': "#0044ff",      # biru
            'hukum': "#ff0000"     # merah
        }
        
        for key, value in self.penukaran.items():
            btn = QPushButton(f"{value['hadiah']} ({value['poin']} poin)")
            btn.clicked.connect(lambda _, k=key: self.tukar_poin(k))
            
            warna = warna_penukaran.get(key, '#bdc3c7')  # default abu-abu
            
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {warna};
                    color: white;
                    font-weight: bold;
                    text-align: left; 
                    padding: 15px;
                    margin: 5px;
                    border: none;
                    border-radius: 8px;
                }}
                QPushButton:hover {{ background-color: #34495e; }}
            """)
            
            vbox.addWidget(btn)
        
        group.setLayout(vbox)
        layout.addWidget(self.poin_label, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(group, 1)
        tab.setLayout(layout)
        return tab

    def create_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.history_list)
        tab.setLayout(layout)
        return tab

    def create_users_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.users_list = QListWidget()
        self.users_list.setStyleSheet("font-family: monospace;")
        layout.addWidget(QLabel("Daftar Pengguna:"))
        layout.addWidget(self.users_list)
        tab.setLayout(layout)
        return tab

    def update_users_list(self):
        self.users_list.clear()
        for user in self.users:
            item = QListWidgetItem(f"{user}: {self.users[user]['poin']} poin")
            self.users_list.addItem(item)

    def select_user(self, name):
        self.current_user = name
        self.update_display()

    def add_user(self):
        new_user = self.new_user_input.text().strip()
        if not new_user:
            QMessageBox.warning(self, "Error", "Nama tidak boleh kosong!")
            return
        if new_user in self.users:
            QMessageBox.warning(self, "Error", "Pengguna sudah ada!")
            return
        
        self.users[new_user] = {'poin': 0.0, 'history': []}
        self.user_combo.addItem(new_user)
        self.user_combo.setCurrentText(new_user)
        self.new_user_input.clear()
        self.save_database()
        self.update_users_list()

    def update_display(self):
        if self.current_user:
            user = self.users[self.current_user]
            self.poin_label.setText(f"Poin Saat Ini: {user['poin']} poin")
            self.status_label.setText(f"Selamat datang, {self.current_user}! | Total Poin: {user['poin']}")
            self.history_list.clear()
            self.history_list.addItems(reversed(user['history']))

    def setor_sampah(self):
        if not self.current_user:
            QMessageBox.warning(self, "Error", "Pilih pengguna terlebih dahulu!")
            return
        
        jenis = self.jenis_combo.currentText().lower()
        berat = self.berat_input.text()
        
        try:
            berat = float(berat)
            if berat <= 0:
                raise ValueError
        except:
            QMessageBox.critical(self, "Error", "Input berat tidak valid!")
            return
        
        if jenis not in self.konversi:
            QMessageBox.warning(self, "Error", "Jenis sampah tidak dikenali!")
            return
        
        poin_tambahan = self.konversi[jenis] * berat
        user = self.users[self.current_user]
        user['poin'] += poin_tambahan
        user['history'].append(f"Setor {berat} kg {jenis} (+{poin_tambahan} poin)")
        
        self.save_database()
        self.update_display()
        QMessageBox.information(self, "Sukses", f"Berhasil menambahkan {poin_tambahan} poin!")

    def tukar_poin(self, jenis):
        if not self.current_user:
            QMessageBox.warning(self, "Error", "Pilih pengguna terlebih dahulu!")
            return
        
        detail = self.penukaran[jenis]
        user = self.users[self.current_user]
        
        if user['poin'] < detail['poin']:
            QMessageBox.warning(self, "Error", "Poin tidak mencukupi!")
            return
        
        confirm = QMessageBox.question(
            self, "Konfirmasi",
            f"Tukar {detail['poin']} poin untuk {detail['hadiah']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            user['poin'] -= detail['poin']
            user['history'].append(f"Tukar poin: {detail['hadiah']} (-{detail['poin']} poin)")
            self.save_database()
            self.update_display()
            QMessageBox.information(self, "Sukses", f"Berhasil menukar {detail['hadiah']}!")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.fullscreen = not self.fullscreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BankSampahApp()
    window.showMaximized()
    sys.exit(app.exec())
