#!/usr/bin/env python3

# https://github.com/noorkhokhar99/How-To-Live-YOLOv5-Model-for-Object-Detection-with-OpenCV/blob/main/YOLOv5Live.py

import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt
import cv2
import process
import os
import random

class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 400, 300)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_widget = QWidget()
        self.stacked_widget.addWidget(self.main_widget)

        layout = QVBoxLayout()
        embedded_layout = QHBoxLayout()

        self.load_button = QPushButton('Load Model', self)
        self.load_button.clicked.connect(self.load_model)

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.clicked.connect(self.upload_image)

        self.random_button = QPushButton('', self)
        self.random_button.clicked.connect(self.random_image)
        self.random_button.setFixedWidth(100)


        self.camera_button = QPushButton('Camera', self)
        self.camera_button.clicked.connect(self.realtime_detect)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.quit)


        layout.addWidget(self.load_button)
        layout.addLayout(embedded_layout)

        embedded_layout.addWidget(self.upload_button)
        embedded_layout.addWidget(self.random_button)

        layout.addWidget(self.camera_button)
        layout.addWidget(self.exit_button)


        self.main_widget.setLayout(layout)

        self.upload_button.setEnabled(False)
        self.camera_button.setEnabled(False)
        self.random_button.setEnabled(False)


    def quit(self):
        app.quit()

    def realtime_detect(self):
        pass

    def random_image(self):
        file_path = "images"
        random_file = random.choice(os.listdir(file_path))
        file_path = os.path.join(file_path, random_file)

        # file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)', options=options)

        if file_path:
            self.image_widget = QWidget()
            self.stacked_widget.addWidget(self.image_widget)

            layout = QVBoxLayout()
            # detect = process.ObjectDetection()
            frame = cv2.imread(file_path)
            results = self.detect.score_frame(frame)
            frame = self.detect.plot_boxes(results, frame)
            convert = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_BGR888)

            original_pixmap = QPixmap(QPixmap.fromImage(convert))
            processed_pixmap = self.process_image(original_pixmap)

            image_label = QLabel()
            image_label.setPixmap(processed_pixmap)
            layout.addWidget(image_label)

            go_back_button = QPushButton('Go Back', self)
            go_back_button.clicked.connect(self.show_main_page)
            layout.addWidget(go_back_button)

            self.image_widget.setLayout(layout)
            self.stacked_widget.setCurrentWidget(self.image_widget)

    def upload_image(self):
        options = QFileDialog.Options()
        # file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp *.gif)', options=options)
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)', options=options)

        if file_path:
            self.image_widget = QWidget()
            self.stacked_widget.addWidget(self.image_widget)

            layout = QVBoxLayout()
            # detect = process.ObjectDetection()
            frame = cv2.imread(file_path)
            results = self.detect.score_frame(frame)
            frame = self.detect.plot_boxes(results, frame)
            convert = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_BGR888)

            original_pixmap = QPixmap(QPixmap.fromImage(convert))
            processed_pixmap = self.process_image(original_pixmap)

            image_label = QLabel()
            image_label.setPixmap(processed_pixmap)
            layout.addWidget(image_label)

            go_back_button = QPushButton('Go Back', self)
            go_back_button.clicked.connect(self.show_main_page)
            layout.addWidget(go_back_button)

            self.image_widget.setLayout(layout)
            self.stacked_widget.setCurrentWidget(self.image_widget)

    def load_model(self):
        self.detect = process.ObjectDetection()
        self.upload_button.setEnabled(True)
        self.camera_button.setEnabled(True)
        self.random_button.setEnabled(True)

        self.load_button.setEnabled(False)
        return

    def process_image(self, pixmap):
        image = pixmap.toImage()
        painter = QPainter()
        painter.begin(image)
        pen = QPen(QColor(Qt.red))
        painter.setPen(pen)
        painter.drawText(20, 20, "Processed Image")
        painter.end()
        return QPixmap.fromImage(image)

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('styles.css').read())
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec_())
