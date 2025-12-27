import sys
import os
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QLabel, QFrame)
from PySide6.QtGui import (QImage, QPixmap, QKeyEvent)
from PySide6.QtCore import Qt
from PIL import Image, ImageGrab, ImageQt

class ModernPasteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quick Image Saver")
        self.setFixedSize(450, 550)
        self.setStyleSheet("background-color: #000000;") # خلفية سوداء

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)

        # 1. العنوان وحالة الحفظ
        self.title_label = QLabel("Single Preview Mode")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.status_label = QLabel("Last saved: None")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #00aba9; font-size: 12px;")
        self.layout.addWidget(self.status_label)

        # 2. زر اللصق
        self.paste_btn = QPushButton("Paste New Image (Ctrl+V)")
        self.paste_btn.setFixedHeight(50)
        self.paste_btn.setCursor(Qt.PointingHandCursor)
        self.paste_btn.setStyleSheet("""
            QPushButton {
                background-color: #00aba9;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #008e8c; }
        """)
        self.paste_btn.clicked.connect(self.handle_paste)
        self.layout.addWidget(self.paste_btn)

        # 3. إطار المعاينة الواحدة (سيتم تحديثه دائماً)
        self.preview_frame = QFrame()
        self.preview_frame.setFixedHeight(300)
        self.preview_frame.setStyleSheet("""
            QFrame {
                border: 2px dashed #333333;
                border-radius: 15px;
                background-color: #0a0a0a;
            }
        """)
        self.preview_layout = QVBoxLayout(self.preview_frame)
        
        self.image_display = QLabel("New image will appear here")
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setStyleSheet("color: #444444; border: none;")
        self.preview_layout.addWidget(self.image_display)
        
        self.layout.addWidget(self.preview_frame)

    def keyPressEvent(self, event: QKeyEvent):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_V:
            self.handle_paste()
        else:
            super().keyPressEvent(event)

    def handle_paste(self):
        try:
            img = ImageGrab.grabclipboard()
            
            if img is None:
                self.status_label.setText("❌ Nothing found in clipboard")
                self.status_label.setStyleSheet("color: #ff4444;")
                return

            # التعامل مع الملفات المنسوخة
            if isinstance(img, list):
                img = Image.open(img[0])

            # 1. إنشاء اسم فريد لكل عملية حفظ لمنع الاستبدال
            timestamp = datetime.now().strftime("%H%M%S") # ساعة دقيقة ثانية
            filename = f"img_{timestamp}.png"
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            save_path = os.path.join(desktop, filename)
            
            # 2. حفظ الصورة
            img.save(save_path, "PNG")

            # 3. تحديث المعاينة (تختفي القديمة وتظهر الجديدة)
            img_rgba = img.convert("RGBA")
            qimage = ImageQt.ImageQt(img_rgba)
            pixmap = QPixmap.fromImage(qimage)
            
            scaled_pixmap = pixmap.scaled(
                self.image_display.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.image_display.setPixmap(scaled_pixmap)
            self.image_display.setText("") # مسح النص التوضيحي
            
            # 4. تحديث نص الحالة
            self.status_label.setText(f"✅ Saved as: {filename}")
            self.status_label.setStyleSheet("color: #00ff88;")

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet("color: #ff4444;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernPasteApp()
    window.show()
    sys.exit(app.exec())