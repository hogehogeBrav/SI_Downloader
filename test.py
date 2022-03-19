import os,sys
import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

baseGround = tk.Tk()
# GUIの画面サイズ
baseGround.geometry('550x200')
#GUIの画面タイトル
baseGround.title('Photo AI Generator')

pb = ttk.Progressbar(baseGround,mode="indeterminate",length=200)

# フォルダ指定の関数
def dirdialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    entry1.set(iDirPath)

def dlPhoto():
  import glob
  from PIL import Image
  import pykakasi
  kakasi = pykakasi.kakasi()

  # 画像名
  value = input1_text.get()
  # 回数
  count = int(input2_text.get())
  # サイズ
  WIDTH = 256
  HEIGHT = 144

  folder_dir = folder1.get()

  def progress():
    pb.start()
    pb.pack()
    pb.place(x=20, y=150)

  def get_photo():
    conv = kakasi.convert(value)
    hepburn_name = conv[0]['hepburn']
    
    from icrawler.builtin import BingImageCrawler
    crawler = BingImageCrawler(storage={"root_dir": os.path.join(folder_dir , value)})
    crawler.crawl(keyword=value , max_num=count)

    dir_name = os.path.join(folder_dir , value)
    new_dir_name = os.path.join(folder_dir , 'resize/' , hepburn_name)
    if not os.path.exists(new_dir_name):
      os.makedirs(new_dir_name)

    for file in os.listdir(dir_name):
      base, ext = os.path.splitext(file)
      if ext == '.jpg':
        print(file)
        #画像の元データを開く
        img = Image.open(os.path.join(dir_name, file))
        #画像を2分の1に縮小
        img_resize = img.resize(size=(WIDTH, HEIGHT))
        #縮小した画像を別フォルダに保存
        img_resize.save(os.path.join(new_dir_name, file))
    #プログレスバー停止
    pb.stop()

  thread1 = threading.Thread(target=progress)
  thread1.start()

  thread2 = threading.Thread(target=get_photo)
  thread2.start()

# テキストボックス１
input1_label = tk.Label(text='集める画像の名前')
input1_label.place(x=20, y=10)
input1_text = tk.Entry()
input1_text.pack()
input1_text.place(x=150, y=10)

#テキストボックス２
input2_label = tk.Label(text='集める枚数')
input2_label.place(x=20, y=40)
input2_text = tk.Entry()
input2_text.insert(0, 20)
input2_text.pack()
input2_text.place(x=150, y=40)

# ボタン
btn = tk.Button(baseGround, text='画像を集める', command=dlPhoto)
btn.pack()
btn.place(x=20, y=110)

# Frame1の作成
frame1 = ttk.Frame(baseGround, padding=10)
frame1.grid(row=0, column=1, sticky=E)
frame1.place(x=0, y=70)

# 「フォルダ参照」ラベルの作成
IDirLabel = ttk.Label(frame1, text="画像保存先＞＞", padding=(5, 2))
IDirLabel.pack(side=LEFT)

# 「フォルダ参照」エントリーの作成
folder1 = StringVar()
IDirEntry = ttk.Entry(frame1, textvariable=folder1, width=30,)
IDirEntry.insert(0, os.path.join(os.environ.get("HOME") , 'Photo AI Generator'))
IDirEntry.pack(side=LEFT)

# 「フォルダ参照」ボタンの作成
IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
IDirButton.pack(side=LEFT)


#表示
baseGround.mainloop()