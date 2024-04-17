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
import pathlib
import platform


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
        self.setWindowTitle('OpenCV Camera')
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


        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            
            start_time = time.perf_counter()
            ret, frame = cap.read()
            if not ret:
                break
            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)
            end_time = time.perf_counter()
            fps = 1 / np.round(end_time - start_time, 3)
            cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            cv2.imshow("img", frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def random_image(self):
        file_path = "images"
        random_file = random.choice(os.listdir(file_path))
        file_path = os.path.join(file_path, random_file)

        # file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)', options=options)

        if file_path:
        # self.stacked_widget = QStackedWidget()
        # self.setCentralWidget(self.stacked_widget)

        # self.main_widget = QWidget()
        # self.stacked_widget.addWidget(self.main_widget)

        # layout = QVBoxLayout()
        # embedded_layout = QHBoxLayout()

            self.image_widget = QWidget()
            self.stacked_widget.addWidget(self.image_widget)

            layout = QVBoxLayout()
            frame = cv2.imread(file_path)
            results = self.detect.score_frame(frame)
            labels, cord = results

            frame = self.detect.plot_boxes(results, frame)
            convert = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_BGR888)

            original_pixmap = QPixmap(QPixmap.fromImage(convert))
            processed_pixmap = self.process_image(original_pixmap)

            image_label = QLabel()
            image_label.setPixmap(processed_pixmap)
            layout.addWidget(image_label)


            go_back_button = QPushButton('Go Back', self)
            go_back_button.clicked.connect(self.show_main_page)

            layout.addWidget(image_label)
            layout.addWidget(go_back_button)

            labels, cord = results
            n = len(labels)
            print("length: " + str(n))
            if n == 0:
                return
            elif n > 1:
                labels = labels[0]
            classs = self.detect.class_to_label(labels)

            x_shape, y_shape = frame.shape[1], frame.shape[0]
            print("x_shape: " + str(x_shape))
            print("y_shape: " + str(y_shape))

            x1 = int(cord[0][0].item()*x_shape)
            y1 = int(cord[0][1].item()*x_shape)
            x2 = int(cord[0][2].item()*x_shape)
            y2 = int(cord[0][3].item()*x_shape)
            precision = cord[0][4].item()

            print("---------------")
            layout1 = QHBoxLayout()
            label1 = QLabel(classs)
            label1_text = QLabel("Class: ")
            # print(labels)
            print("---------------")
            layout2 = QHBoxLayout()
            label2_x1 = QLabel(f"{x1:.2f}")
            label2_y1 = QLabel(f"{y1:.2f}")
            label2_x2 = QLabel(f"{x2:.2f}")
            label2_y2 = QLabel(f"{y2:.2f}")
            label_precision = QLabel(f"{precision:.2f}")

            label2_text = QLabel("Cord: ")
            label2_x1_text = QLabel("x1: ")
            label2_y1_text = QLabel("y1: ")
            label2_x2_text = QLabel("x2: ")
            label2_y2_text = QLabel("y2: ")
            label_precision_text = QLabel("Precision: ")

            self.image_widget.setLayout(layout)
            self.stacked_widget.setCurrentWidget(self.image_widget)

            layout1.addWidget(label1_text)
            layout1.addWidget(label1)
            layout1.addWidget(label_precision_text)
            layout1.addWidget(label_precision)

            layout2.addWidget(label2_text)
            layout2.addWidget(label2_x1_text)
            layout2.addWidget(label2_x1)
            layout2.addWidget(label2_y1_text)
            layout2.addWidget(label2_y1)
            layout2.addWidget(label2_x2_text)
            layout2.addWidget(label2_x2)
            layout2.addWidget(label2_y2_text)
            layout2.addWidget(label2_y2)

            layout.addLayout(layout1)
            layout.addLayout(layout2)

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

            go_back_button = QPushButton('Go Back', self)
            go_back_button.clicked.connect(self.show_main_page)

            layout.addWidget(image_label)
            layout.addWidget(go_back_button)

            labels, cord = results
            n = len(labels)
            print("length: " + str(n))
            if n == 0:
                return
            elif n > 1:
                labels = labels[0]
            classs = self.detect.class_to_label(labels)

            x_shape, y_shape = frame.shape[1], frame.shape[0]
            print("x_shape: " + str(x_shape))
            print("y_shape: " + str(y_shape))
            # # for i in range(n):
            # # row = cord
            # #     if row[4] >= 0.2:
            # print(x_shape)
            # x1 = int(cord[0])
            # x1, y1, x2, y2 = int(cord[0]*x_shape), int(cord[1]*y_shape), int(cord[2]*x_shape), int(cord[3]*y_shape)
            x1 = int(cord[0][0].item()*x_shape)
            y1 = int(cord[0][1].item()*x_shape)
            x2 = int(cord[0][2].item()*x_shape)
            y2 = int(cord[0][3].item()*x_shape)
            precision = cord[0][4].item()
            # #         # bgr = (0, 255, 0)
            print("---------------")
            layout1 = QHBoxLayout()
            label1 = QLabel(classs)
            label1_text = QLabel("Class: ")
            # print(labels)
            print("---------------")
            layout2 = QHBoxLayout()
            # label2_x1 = QLabel("x1")
            label2_y1 = QLabel("y1")
            label2_x2 = QLabel("x2")
            label2_y2 = QLabel("y2")
            label2_x1 = QLabel(f"{x1:.2f}")
            label2_y1 = QLabel(f"{y1:.2f}")
            label2_x2 = QLabel(f"{x2:.2f}")
            label2_y2 = QLabel(f"{y2:.2f}")
            print("---------------")
            label_precision = QLabel(f"{precision:.2f}")
            print("Precision: " + str( precision ))
            

            label2_text = QLabel("Cord: ")
            label2_x1_text = QLabel("x1: ")
            label2_y1_text = QLabel("y1: ")
            label2_x2_text = QLabel("x2: ")
            label2_y2_text = QLabel("y2: ")
            label_precision_text = QLabel("Precision: ")
            # cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
            # print(cord)

            # frame = self.detect.plot_boxes(results, frame)

            self.image_widget.setLayout(layout)
            self.stacked_widget.setCurrentWidget(self.image_widget)

            layout1.addWidget(label1_text)
            layout1.addWidget(label1)
            layout1.addWidget(label_precision_text)
            layout1.addWidget(label_precision)

            layout2.addWidget(label2_text)
            layout2.addWidget(label2_x1_text)
            layout2.addWidget(label2_x1)
            layout2.addWidget(label2_y1_text)
            layout2.addWidget(label2_y1)
            layout2.addWidget(label2_x2_text)
            layout2.addWidget(label2_x2)
            layout2.addWidget(label2_y2_text)
            layout2.addWidget(label2_y2)

            layout.addLayout(layout1)
            layout.addLayout(layout2)

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
    if platform.system() == 'Windows':
        temp = pathlib.PosixPath
        pathlib.PosixPath = pathlib.WindowsPath

    app = QApplication(sys.argv)
    # app.setStyleSheet(open('styles.css').read())
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec_())
