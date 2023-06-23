from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QPushButton, QTextEdit, QCheckBox, QMessageBox, QFileDialog, QVBoxLayout, QWidget, QDialog
from PyQt5.QtGui import QColor, QTextOption, QPalette, QPixmap, QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL.ImageQt import ImageQt
from generator import PasswordGenerator

import pyperclip
import qrcode
import sys
import os

ICON_File = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")

class PasswordGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор паролей")
        self.setWindowIcon(QIcon(ICON_File))
        self.setGeometry(100, 100, 570, 400)
        self.setFixedSize(self.size())

        # Set background color
        self.set_background_color("#181818")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.length_slider = QSlider(Qt.Horizontal, self.central_widget)
        self.length_slider.setRange(1, 150)
        self.length_slider.setValue(8)
        self.style_slider(self.length_slider)
        self.layout.addWidget(self.length_slider)
        self.length_slider.valueChanged.connect(self.generate_password)

        self.length_label = QLabel(f"Длина пароля: {str(self.length_slider.value())} символов", self.central_widget)
        self.style_label(self.length_label)
        self.layout.addWidget(self.length_label)

        self.digits_checkbox = QCheckBox("Использовать цифры", self.central_widget)
        self.style_checkbox(self.digits_checkbox)
        self.layout.addWidget(self.digits_checkbox)
        self.digits_checkbox.setChecked(True)
        self.digits_checkbox.stateChanged.connect(self.generate_password)

        self.letters_checkbox = QCheckBox("Использовать буквы", self.central_widget)
        self.style_checkbox(self.letters_checkbox)
        self.layout.addWidget(self.letters_checkbox)
        self.letters_checkbox.stateChanged.connect(self.generate_password)

        self.special_chars_checkbox = QCheckBox("Использовать спецсимволы", self.central_widget)
        self.style_checkbox(self.special_chars_checkbox)
        self.layout.addWidget(self.special_chars_checkbox)
        self.special_chars_checkbox.stateChanged.connect(self.generate_password)

        self.password_textbox = QTextEdit(self.central_widget)
        self.style_textbox(self.password_textbox)
        self.layout.addWidget(self.password_textbox)

        self.max_length = 150  # Максимальное количество символов
        self.password_textbox.textChanged.connect(self.limit_text_length)

        self.copy_button = QPushButton("Копировать", self.central_widget)
        self.style_button(self.copy_button)
        self.layout.addWidget(self.copy_button)
        self.copy_button.clicked.connect(self.copy_password)

        self.save_button = QPushButton("Сохранить", self.central_widget)
        self.style_button(self.save_button)
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_password)

        self.save_button = QPushButton("Сгенерировать QR", self.central_widget)
        self.style_button(self.save_button)
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.qr_generate)

        self.generate_password()

    def limit_text_length(self):
        text = self.password_textbox.toPlainText()
        if len(text) > self.max_length:
            self.password_textbox.setPlainText(text[:self.max_length])

    def set_background_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

    def style_label(self, label):
        label.setStyleSheet("color: #ffffff; font-size: 12pt;")

    def style_slider(self, slider):
        slider.setStyleSheet(
            "QSlider::groove:horizontal {"
            "background-color: #ffffff;"
            "height: 6px;"
            "border-radius: 3px;"
            "}"

            "QSlider::handle:horizontal {"
            "background-color: #1E90FF;"
            "width: 10px;"
            "border-radius: 5px;"
            "margin: -5px 0px;"
            "}"
        )

    def style_checkbox(self, checkbox):
        checkbox.setStyleSheet(
            "QCheckBox {"
            "color: #ffffff;"
            "font-size: 10pt;"
            "}"

            "QCheckBox::indicator {"
            "width: 18px;"
            "height: 18px;"
            "}"

            "QCheckBox::indicator:checked {"
            "background-color: #1E90FF;"
            "border: 1px solid #1E90FF;"
            "}"

            "QCheckBox::indicator:unchecked {"
            "background-color: transparent;"
            "border: 1px solid #1E90FF;"
            "}"
        )

    def style_textbox(self, textbox):
        textbox.setStyleSheet(
            "QTextEdit {"
            "background-color: #ffffff;"
            "color: #000000;"
            "font-size: 10pt;"
            "}"
        )

    def style_button(self, button):
        button.setStyleSheet(
            "QPushButton {"
            "background-color: #1E90FF;"
            "color: #ffffff;"
            "font-size: 10pt;"
            "border: none;"
            "border-radius: 5px;"
            "padding: 8px;"
            "}"

            "QPushButton:hover {"
            "background-color: #4169E1;"
            "}"
        )

    def generate_password(self):
        try:
            length = self.length_slider.value()
            use_digits = self.digits_checkbox.isChecked()
            use_letters = self.letters_checkbox.isChecked()
            use_special_chars = self.special_chars_checkbox.isChecked()
            self.length_label.setText(f"Длина пароля: {str(self.length_slider.value())} символов")
            generator = PasswordGenerator(length, use_digits, use_letters, use_special_chars)
            password = generator.generate_password()
            self.password_textbox.setPlainText(password)
        except ValueError:
            pass
        

    def copy_password(self):
        password = self.password_textbox.toPlainText().strip()
        if password:
            pyperclip.copy(password)
        else:
            pass

    def save_password(self):
        password = self.password_textbox.toPlainText().strip()
        if password:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить пароль", "", "Password Files (*.key);;Text Files (*.txt)", options=QFileDialog.Options())
            if file_path:
                try:
                    with open(file_path, "w") as file:
                        file.write(password)
                    QMessageBox.information(self, "Сохранено", "Пароль успешно сохранен в файл.")
                except IOError:
                    QMessageBox.critical(self, "Ошибка", "Не удалось сохранить файл.")
        else:
            QMessageBox.warning(self, "Пустой пароль", "Сначала сгенерируйте пароль.")

    def qr_generate(self):
        password = self.password_textbox.toPlainText().strip()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(password)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
        pixmap = QPixmap.fromImage(ImageQt(qr_image))

        self.qr_window = QRCodeWindow(pixmap)
        self.qr_window.show()

class QRCodeWindow(QDialog):
    def __init__(self, pixmap):
        super().__init__()
        self.setWindowTitle("QR код")
        self.setWindowIcon(QIcon(ICON_File))
        layout = QVBoxLayout(self)
        label = QLabel(self)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        self.setLayout(layout)
        self.adjustSize()

        self.save_button = QPushButton("Сохранить QR", self)
        self.save_button.clicked.connect(self.save_qr_code)
        layout.addWidget(self.save_button)

    def update_qr_code(self, pixmap):
        label = self.layout.itemAt(0).widget()
        label.setPixmap(pixmap)

    def save_qr_code(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить QR", "", "Image Files (*.png)")
        if file_path:
            pixmap = self.layout().itemAt(0).widget().pixmap()
            pixmap.save(file_path)
            QMessageBox.information(self, "Сохранено", "QR-код успешно сохранен в файл.")
        else:
            QMessageBox.warning(self, "Отменено", "Сохранение QR-кода отменено.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    gui = PasswordGeneratorGUI()
    gui.show()

    sys.exit(app.exec_())
