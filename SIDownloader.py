from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from email.mime import base
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
from turtle import left
from pyrsistent import b

from setuptools import Command

baseGround = tk.Tk()
# GUIの画面サイズ
baseGround.geometry('550x450')
# ウインドウサイズ固定
baseGround.resizable(width=False, height=False)
# 背景色
# baseGround.configure(bg='white')
# GUIの画面タイトル
baseGround.title('Simple Image Downloader')

flag = BooleanVar()
flag.set(True)

# フォルダ指定の関数
def dirdialog_clicked():
  iDir = os.path.abspath(os.path.dirname(__file__))
  iDir = folder1.get()
  iDirPath = filedialog.askdirectory(initialdir = iDir)
  if iDirPath:
    folder1.set(iDirPath)
  else:
    folder1.set(iDir)

# プログレスバー開始
def progress():
  pb.start()
  pb_label['text'] = "画像収集中..."

def txt_chk():
  flg = True
  if not input1_text.get():
    messagebox.showinfo('' , '画像の名前を入力してください。')
    flg = False
  if not input2_text.get():
    messagebox.showinfo('' , '集める枚数を入力してください。')
    flg = False
  if flag.get():
    if not resize_folder_text.get():
      messagebox.showinfo('' , 'リサイズ画像の保存先フォルダ名を入力してください。')
      flg = False
    if not resize_width_text.get():
      messagebox.showinfo('' , '横幅を入力してください。')
      flg = False
    if not resize_height_text.get():
      messagebox.showinfo('' , '縦幅を入力してください。')
      flg = False
  if flg:
    thread1 = threading.Thread(target=progress)
    thread1.start()

    thread2 = threading.Thread(target=dl_photo)
    thread2.start()

# 画像ダウンロード
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
  if flag.get():
    WIDTH = int(resize_width_text.get())
    HEIGHT = int(resize_height_text.get())
  # ディレクトリ
  folder_dir = folder1.get()
  # リサイズフォルダ名
  resize_dir = resize_folder_text.get()

  conv = kakasi.convert(value)
  hepburn_name = conv[0]['hepburn']
  
  from icrawler.builtin import BingImageCrawler
  crawler = BingImageCrawler(storage={"root_dir": os.path.join(folder_dir , value)})
  crawler.crawl(keyword=value , max_num=count)

  # リサイズ処理
  if flag.get():
    pb_label['text'] = "リサイズ中..."
    dir_name = os.path.join(folder_dir , value)
    new_dir_name = os.path.join(folder_dir , resize_dir , hepburn_name)
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

# ディレクトリチェック
def photo_dirchk():
  folder_dir = folder1.get()
  folder = os.listdir(folder_dir)
  print(os.listdir(folder_dir))
  dir = [f for f in folder if os.path.isdir(os.path.join(folder_dir, f))]
  lists = tk.StringVar(value=dir)
  
  if len(dir) == 0:
    messagebox.showinfo('収集済みの画像名' , '選択されたディレクトリには画像がダウンロードされていません。')
  else:
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

# リサイズチェックボックス
def change_state():
  if flag.get():
      new_state = 'normal'
  else:
    new_state = 'disabled'
  resize_folder_label.configure(state = new_state)
  resize_folder_text.configure(state = new_state)
  resize_width_label.configure(state = new_state)
  resize_width_text.configure(state = new_state)
  resize_height_label.configure(state = new_state)
  resize_height_text.configure(state = new_state)

# 画像設定フレーム
frame_main = tk.LabelFrame(baseGround , text="画像設定" , fg="green")
frame_main.grid(row=0, column=1, sticky=E)
frame_main.place(x=10, y=10)

frame_photoname = ttk.Frame(frame_main , padding=5)
frame_photoname.grid(row=0, column=1, sticky=E)

frame_photocnt = ttk.Frame(frame_main , padding=5)
frame_photocnt.grid(row=1, column=1, sticky=E)

# テキストボックス１
input1_label = tk.Label(frame_photoname , text='集める画像の名前' , width=20 , anchor=tk.W)
input1_label.pack(side=LEFT)
# input1_label.place(x=20, y=10)
input1_text = tk.Entry(frame_photoname)
input1_text.pack(side=LEFT)
# input1_text.place(frame_main , x=150, y=10)

#テキストボックス２
input2_label = tk.Label(frame_photocnt , text='集める枚数' , width=20 , anchor=tk.W)
input2_label.pack(side=LEFT)
# input2_label.place(x=20, y=40)
input2_text = tk.Entry(frame_photocnt)
input2_text.insert(0, 20)
input2_text.pack(side=LEFT)
# input2_text.place(x=150, y=40)


frame_resize = tk.LabelFrame(baseGround , labelwidget=Checkbutton(baseGround , text="リサイズする" , variable=flag, command=change_state))
frame_resize.place(x=10 , y=120)

frame_resizefolder = ttk.Frame(frame_resize , padding=5)
frame_resizefolder.grid(row=0, column=1, sticky=E)

frame_resizeheight = ttk.Frame(frame_resize , padding=5)
frame_resizeheight.grid(row=1, column=1, sticky=E)

frame_resizewidth = ttk.Frame(frame_resize , padding=5)
frame_resizewidth.grid(row=2, column=1, sticky=E)

# 保存先フォルダ名
resize_folder_label = tk.Label(frame_resizefolder , text='保存先フォルダ名' , width=20 , anchor=tk.W , state="normal")
resize_folder_label.pack(side=LEFT)
resize_folder_text = tk.Entry(frame_resizefolder , state="normal")
resize_folder_text.insert(0 , "resize")
resize_folder_text.pack(side=LEFT)

# 縦幅
resize_height_label = tk.Label(frame_resizeheight , text='縦幅(ピクセル)' , width=20 , anchor=tk.W , state="normal")
resize_height_label.pack(side=LEFT)
resize_height_text = tk.Entry(frame_resizeheight , state="normal")
resize_height_text.insert(0 , 144)
resize_height_text.pack(side=LEFT)

# 横幅
resize_width_label = tk.Label(frame_resizewidth , text='横幅(ピクセル)' , width=20 , anchor=tk.W , state="normal")
resize_width_label.pack(side=LEFT)
resize_width_text = tk.Entry(frame_resizewidth , state="normal")
resize_width_text.insert(0 , 256)
resize_width_text.pack(side=LEFT)


# Frame1の作成
frame1 = tk.LabelFrame(baseGround, text="保存先ディレクトリ設定" , fg="blue")
frame1.grid(row=0, column=1, sticky=E)
frame1.place(x=10, y=280)

# 「フォルダ参照」ラベルの作成
IDirLabel = ttk.Label(frame1, text="画像保存先＞＞", padding=(5, 2))
IDirLabel.pack(side=LEFT)

# 「フォルダ参照」エントリーの作成
folder1 = StringVar()
IDirEntry = ttk.Entry(frame1, textvariable=folder1, width=30,)
IDirEntry.insert(0, os.path.join(os.path.expanduser("~") , 'Simple Image Downloader'))
IDirEntry.pack(side=LEFT)

# 「フォルダ参照」ボタンの作成
IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
IDirButton.pack(side=LEFT)


# 画像収集ボタン
btn = tk.Button(baseGround, text='画像を収集', command=txt_chk)
btn.pack()
btn.place(x=20, y=340)

# 種類確認ボタン
btn2 = tk.Button(baseGround, text='収集済みの画像名を確認', command=photo_dirchk)
btn2.pack()
btn2.place(x=120, y=340)

pb = ttk.Progressbar(baseGround,mode="indeterminate",length=200)
pb.pack()
pb.place(x=20, y=380)

pb_label = tk.Label(text='待機中')
pb_label.pack()
pb_label.place(x=250, y=380)

#表示
baseGround.mainloop()