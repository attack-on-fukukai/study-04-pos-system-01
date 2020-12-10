import pandas as pd
import sys
import datetime

### 商品クラス
class Item:
    def __init__(self,code,name,price):
        self.code = code
        self.name = name
        self.price = price

    def get_code(self):
    # 商品コードを返す
        return self.code

    def get_name(self):
    # 商品名を返す
        return self.name

    def get_price(self):
    # 価格を返す
        return self.price

### 商品マスタクラス
class ItemMaster:
    def __init__(self):
        self.item_master = []

    def addItem(self,item):
    #商品クラスを追加する

        self.item_master.append(item)

    def getMenu(self):
    # メニューを表示する
        print("*** メニュー ***")
        for item in self.item_master:
            print("{} {} {}円".format(item.get_code(),item.get_name(),item.get_price()))

    def searchItem(self,code):
    # 商品コードをキーに商品マスタを検索する
        for item in self.item_master:
            if item.get_code() == code:
                return item

### オーダークラス
class Order:
    def __init__(self,item_master):

        # 受注した商品
        self.code = ""      # 商品コード
        self.name = ""      # 商品名
        self.price = ""      # 価格

        # 受注計算結果
        self.goukei = 0     # 合計
        self.oazukari = 0   # お預かり
        self.oturi = 0      # おつり

        self.item_master = item_master
        self.item_order_list=[]

    def add_item_order(self,code,kosu):
    # オーダーを追加する
        self.item_order_list.append([code,kosu])

    def view_item_list(self):
    # オーダー内容を表示する
        for item in self.item_order_list:
            orderCord = item[0]
            orderKosu = item[1]

            # 商品コードからマスタ情報を取得する
            master = self.item_master.searchItem(orderCord)           

            if master is None:
                print("商品コード:{}は当店では取り扱っていない商品です。".format(orderCord))
                sys.exit(0)
            else:
                print("*** 注文内容 ***")
                #商品コードを表示する
                print("商品コード:{}".format(master.get_code()))
                #商品名を表示する
                print("商品名:{}".format(master.get_name()))
                #価格を表示する
                print("価格:{}".format(master.get_price()))
                #個数を表示する
                print("個数:{}".format(orderKosu))
                #合計金額を表示する
                self.goukei = int(orderKosu) * master.get_price()
                print("合計金額:{}円になります。".format(self.goukei))

    def getOturi(self,oazukari):
    # おつりを計算する
        self.oazukari = int(oazukari)
        self.oturi = self.oazukari - self.goukei
        return self.oturi

    def createReceipt(self):
    # レシートを発行する
        fileName = "{:%Y%m%d%H%M%S}.csv".format(datetime.datetime.now())
        receipt = open(fileName, "w", encoding="UTF-8")

        for item in self.item_order_list:
            orderCord = item[0]
            orderKosu = item[1]

            # 商品コードからマスタ情報を取得する
            master = self.item_master.searchItem(orderCord)           

            text = "*** 領収書 ***\n"
            text += "商品コード:{}\n".format(master.get_code())
            text += "商品名:{}\n".format(master.get_name())
            text += "価格:{}\n".format(master.get_price())
            text += "個数:{}\n".format(orderKosu)

            text += "合計金額:{}円\n".format(self.goukei)
            text += "お預かり金額:{}円\n".format(self.oazukari)
            text += "おつり:{}円".format(self.oturi)
            
        receipt.write(text)
        receipt.close

### メイン処理
def main():
    # マスタファイルを読み込む
    try:
        df = pd.read_csv("item_mast.csv",dtype={"商品コード":str,"商品名":str,"価格":int})
    except FileNotFoundError:
        print("マスタファイルが見つかりませんでした")
        sys.exit(0)

    item_master = ItemMaster()
    for code, name, kakaku in zip(df["商品コード"], df["商品名"], df["価格"]):
        item_master.addItem(Item(code,name,kakaku))

    print("いらっしゃいませ！")
    print("メニューはこちらです。")
    item_master.getMenu()

    print("")
    
    code = input("何にしますか？商品コードで入力してください。")
    if len(code) == 0:
        print("オーダーを確認できませんでした")
        sys.exit(0)
    else:
        kosu = input("個数を入力してください。")
        if len(kosu) == 0:
            print("個数を確認できませんでした")
            sys.exit(0)

    # オーダー登録   
    order = Order(item_master)
    order.add_item_order(code,kosu)

    # オーダー表示
    order.view_item_list()

    # おつりを計算する
    oazukari = input("いくら払いますか？")
    oturi = order.getOturi(oazukari)
    if oturi == 0:
        print("ちょうどですね。ありがとうございました！")
    elif oturi > 0:
        print("おつり{}円になります。ありがとうございました！".format(oturi))
    else:
        print("お客さん、お金が足りませんよ！")
        sys.exit(0)
        
    # レシートを発行
    order.createReceipt()

if __name__ == "__main__":
    main()