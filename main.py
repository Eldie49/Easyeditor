#подключи нужные модули PIL
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtWidgets import *
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle("Eazy EДитор")

folder_btn = QPushButton("Папка")
img_list = QListWidget()
picture = QLabel("Картинка")
left_btn = QPushButton("Лево")
right_btn = QPushButton("Право")
mirror_btn = QPushButton("Зеркало")
sharp_btn = QPushButton("Резкость")
bw_btn = QPushButton("Ч/Б")
rs_btn = QPushButton("Размытие")


layout_1 = QVBoxLayout()
layout_1.addWidget(folder_btn)
layout_1.addWidget(img_list)

layout_2 = QHBoxLayout()
layout_2.addWidget(left_btn)
layout_2.addWidget(rs_btn)
layout_2.addWidget(right_btn)
layout_2.addWidget(mirror_btn)
layout_2.addWidget(sharp_btn)
layout_2.addWidget(bw_btn)

layout_3 = QVBoxLayout()
layout_3.addWidget(picture)
layout_3.addLayout(layout_2)

layout_4 = QHBoxLayout()
layout_4.addLayout(layout_1 , stretch=1)
layout_4.addLayout(layout_3,stretch=5)


main_win.setLayout(layout_4)



workdir = ""
def choose_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files , extentions):
    result = []
    for f in files:
        for ext in extentions:
            if f.endswith(ext):
                result.append(f)
    return result
def show_filenames_list():
    extentions = [".jpg",".jpeg",".png",".bmp",".gif"]
    choose_workdir()
    img_list.clear()
    filenames = filter(os.listdir(workdir), extentions)
    print(filenames)
    for filename in filenames:
        img_list.addItem(filename)



class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def load_image(self, dir, filename):
        self.filename = filename
        self.dir = dir
        img_path = os.path.join(dir, filename)
        print()
        print(img_path)
        print()
        self.image = Image.open(img_path)
    def show_image(self, path):
        picture.hide()
        pix_img = QPixmap(path)
        w, h = picture.width(),picture.height()
        pix_img = pix_img.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pix_img)
        picture.show()
    def save_image(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        img_path = os.path.join(path, self.filename)
        self.image.save(img_path)
    def do_bw(self):
        self.image = self.image.convert('L')
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_left(self):

        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_rs(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)

    def do_scharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)
    
    def do_rs_btn(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_image()
        path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(path)
rs_btn
workimage  = ImageProcessor()
def show_chosen_image():
    if img_list.currentRow() >= 0:
        filename = img_list.currentItem().text()
        workimage.load_image(workdir, filename)
        img_path = os.path.join(workimage.dir, workimage.filename)
        workimage.show_image(img_path)
folder_btn.clicked.connect(show_filenames_list)
img_list.currentRowChanged.connect(show_chosen_image)
bw_btn.clicked.connect(workimage.do_bw)
left_btn.clicked.connect(workimage.do_left)
right_btn.clicked.connect(workimage.do_right)
mirror_btn.clicked.connect(workimage.do_rs)
sharp_btn.clicked.connect(workimage.do_scharpen)
rs_btn.clicked.connect(workimage.do_rs_btn)


main_win.showMaximized()
app.exec()