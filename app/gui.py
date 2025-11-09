from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from .mood_detector import detect_mood
from .music_recommender import recommend_songs

class PhotoMusicApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo → Music App")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

        self.current_photo = None

        # Outer layout (centers everything)
        outer_layout = QHBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)

        # Frame to mimic a mini gadget
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #181818;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        frame.setFixedSize(480, 560)

        # Inner layout for content
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # Photo display
        self.photo_label = QLabel("Upload a photo to get started")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setFixedSize(420, 240)
        self.photo_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #333;
                border-radius: 12px;
                background-color: #202020;
                font-size: 14px;
                color: #AAAAAA;
            }
        """)
        layout.addWidget(self.photo_label)

        # Upload button
        self.upload_btn = QPushButton("Upload Photo")
        self.upload_btn.setStyleSheet(self.button_style())
        self.upload_btn.clicked.connect(self.upload_photo)
        layout.addWidget(self.upload_btn)

        # Mood label
        self.mood_label = QLabel("Detected mood: N/A")
        self.mood_label.setAlignment(Qt.AlignCenter)
        self.mood_label.setFont(QFont("Arial", 12))
        self.mood_label.setStyleSheet("color: #1DB954;")
        layout.addWidget(self.mood_label)

        # Get recommendations button
        self.recommend_btn = QPushButton("🎧 Get Music Recommendations")
        self.recommend_btn.setStyleSheet(self.button_style())
        self.recommend_btn.clicked.connect(self.get_recommendations)
        layout.addWidget(self.recommend_btn)

        # Song list
        self.songs_list = QListWidget()
        self.songs_list.setStyleSheet("""
            QListWidget {
                background-color: #181818;
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #1DB954;
                color: black;
            }
        """)
        layout.addWidget(self.songs_list)

        frame.setLayout(layout)
        outer_layout.addWidget(frame)
        self.setLayout(outer_layout)

    def button_style(self):
        return """
            QPushButton {
                background-color: #1DB954;
                border: none;
                color: black;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1ED760;
            }
        """
    
    def upload_photo(self):
        
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Photo", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.current_photo = file_name
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(self.photo_label.width(), self.photo_label.height())
            self.photo_label.setPixmap(pixmap)
            self.photo_label.setText("") 
            
            self.mood_label.setText("Detected mood: N/A")
            self.songs_list.clear()
    
    def get_recommendations(self):
        if not self.current_photo:
            return  
        
        detected_mood = detect_mood(self.current_photo)
        self.mood_label.setText(f"Detected mood: {detected_mood}")
        
        songs = recommend_songs(detected_mood)
        self.songs_list.clear()
        

        song_strings = [f"{name} — {artist}" for name, artist in songs]
        self.songs_list.addItems(song_strings)

       
