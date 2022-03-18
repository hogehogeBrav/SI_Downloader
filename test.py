import tkinter as tk

def btn_click():
  # 入力した値を取得
  text1 = input_text.get()
  # 入力した値をラベルに出力
  label2['text'] = text1

def dlPhoto():
  import os
  import glob
  from PIL import Image
  import pykakasi

  kakasi = pykakasi.kakasi()

  # 画像名
  value = input1_text.get()

  # 回数
  count = int(input2_text.get())

  WIDTH = 256
  HEIGHT = 144

  folder_dir = './'

  def get_photo(folder_dir , value_name , count):
    conv = kakasi.convert(value_name)
    hepburn_name = conv[0]['hepburn']
    
    from icrawler.builtin import BingImageCrawler
    crawler = BingImageCrawler(storage={"root_dir": os.path.join(folder_dir , value_name)})
    crawler.crawl(keyword=value_name , max_num=count)

    dir_name = os.path.join(folder_dir , value_name)
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

  get_photo(folder_dir , value , count)

baseGround = tk.Tk()
# GUIの画面サイズ
baseGround.geometry('300x200')
#GUIの画面タイトル
baseGround.title('Photo AI Generator')

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
input2_text.insert(0, 200)
input2_text.pack()
input2_text.place(x=150, y=40)

# ボタン
btn = tk.Button(baseGround, text='画像を集める', command=dlPhoto)
btn.pack()
btn.place(x=20, y=80)

# # ラベル
# label1 = tk.Label(text = '入力値:')
# label1.pack()
# label1.place(x=20, y=120)

# label2 = tk.Label()
# label2.pack()
# label2.place(x=20, y=140)

#表示
baseGround.mainloop()