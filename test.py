from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from importlib.util import set_loader
from lib2to3.pgen2.pgen import generate_grammar
import os,sys
from socket import inet_aton
import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from setuptools import Command

baseGround = tk.Tk()
# GUIの画面サイズ
baseGround.geometry('550x230')
# GUIの画面タイトル
baseGround.title('Photo AI Generator')

# フォルダ指定の関数
def dirdialog_clicked():
  iDir = os.path.abspath(os.path.dirname(__file__))
  iDirPath = filedialog.askdirectory(initialdir = iDir)
  entry1.set(iDirPath)

def progress():
  pb.start()
  pb_label['text'] = "画像収集中..."

def dl_photo():
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
  # ディレクトリ
  folder_dir = folder1.get()

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
    pb_label['text'] = "完了"

  thread1 = threading.Thread(target=progress)
  thread1.start()

  thread2 = threading.Thread(target=get_photo)
  thread2.start()

def photo_dirchk():
  folder_dir = os.path.join(folder1.get() , 'resize')
  folder = os.listdir(folder_dir)
  dir = [f for f in folder if os.path.isdir(os.path.join(folder_dir, f))]
  lists = tk.StringVar(value=dir)
  # for index, item in enumerate(dir):
  #   print("インデックス：" + str(index) + ", 値：" + item)
  #   value = tk.Label(dirchk, text = 'インデックス：' + str(index) + ',  名前：' +item)
  #   value.pack()
  #   value.place(x=30 , y=(23 * (index + 1)))
  
  # 画面生成
  dirchk = tk.Toplevel()
  dirchk.geometry('300x380')
  # ウインドウサイズ固定
  dirchk.resizable(width=False, height=False)
  # 親ウインドウ操作不能にする
  dirchk.grab_set()
  #GUIの画面タイトル
  dirchk.title('収集済みの画像名')
  # flame
  dirchk_flame = ttk.Frame(dirchk)
  dirchk_flame.pack(pady=20)
  # 種類数
  count = tk.Label(dirchk, text=str(len(dir)) + '種類')
  count.pack()
  # 各種ウィジェットの作成
  Listbox = tk.Listbox(dirchk_flame, listvariable=lists, height=15)
  # スクロールバーの作成
  scrollbar = tk.Scrollbar(dirchk_flame, orient=tk.VERTICAL, command=Listbox.yview)
  # スクロールバーをListboxに反映
  Listbox["yscrollcommand"] = scrollbar.set
  # 各種ウィジェットの設置
  Listbox.grid(row=0, column=0)
  scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
  # 閉じるボタン
  button = tk.Button(dirchk, text = '閉じる', command=dirchk.destroy)
  button.pack()


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

# 画像収集ボタン
btn = tk.Button(baseGround, text='画像を収集', command=dl_photo)
btn.pack()
btn.place(x=20, y=120)

# 種類確認ボタン
btn2 = tk.Button(baseGround, text='収集済みの画像名を確認', command=photo_dirchk)
btn2.pack()
btn2.place(x=120, y=120)

# Frame1の作成
frame1 = ttk.Frame(baseGround, padding=10)
frame1.grid(row=0, column=1, sticky=E)
frame1.place(x=5, y=70)

# 「フォルダ参照」ラベルの作成
IDirLabel = ttk.Label(frame1, text="画像保存先＞＞", padding=(5, 2))
IDirLabel.pack(side=LEFT)

# 「フォルダ参照」エントリーの作成
folder1 = StringVar()
IDirEntry = ttk.Entry(frame1, textvariable=folder1, width=30,)
IDirEntry.insert(0, os.path.join(os.path.expanduser("~") , 'Photo AI Generator'))
IDirEntry.pack(side=LEFT)

# 「フォルダ参照」ボタンの作成
IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
IDirButton.pack(side=LEFT)

pb = ttk.Progressbar(baseGround,mode="indeterminate",length=200)
pb.pack()
pb.place(x=20, y=180)

pb_label = tk.Label(text='待機中')
pb_label.pack()
pb_label.place(x=250, y=180)

#表示
baseGround.mainloop()