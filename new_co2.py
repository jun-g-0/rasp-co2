#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import datetime

# シリアル操作に使用する変数を初期化
s = None

# デバイスの立ち上げ命令
def setup():
    global s # global変数として扱う旨宣言、readdataからもアクセス可能に(Import下のsと同一オブジェクトに)
    # 使用するポート等を記入し、初期化
    # pySerial API
    # https://pythonhosted.org/pyserial/pyserial_api.html
    # Raspberry Pi Documentation
    # https://www.raspberrypi.com/documentation/computers/configuration.html
    s = serial.Serial('/dev/ttyAMA0',baudrate=9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1.0)
    # 5秒ほどのスタンバイで充分、あとでCDによるフィルターがあるため、神経質にならずとも良い
    time.sleep(5)
    # 起動できた旨、コンソールに出力
    print(s)

def readdata():
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # ファイル名はデータ行数が、1日で高々1万行(10秒に1回=6*60*24)のため、固定の名前とした
    saveFileName = '/home/pi/Desktop/co2data/co2.txt' # + datetime.datetime.now().strftime("%Y%m") + 'CO2data.txt'
    
    # センターの戻り値を格納
    b = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    s.write(b)
    time.sleep(5)
    
    # 格納された戻り値を処理、ラグがあったためSleepを置いた記憶
    result = s.read(9)
    time.sleep(5)
    # printはデバッグのための内容確認(以下同様)
    print(result)
    print(len(result))

    # resultが9桁入ってきた時点でほぼまともじゃないデータは弾かれており、
    # ほとんど意味を成していなかったため、チェックサム確認を無効
    if len(result) >= 9:
        print(result[2])
        print(result[3])

        #checksum = (0xFF*1 - ((result[1]*1+result[2]*1+result[3]*1+result[4]*1+result[5]*1+result[6]*1+result[7]*1)% 256))+ 0x01*1
        #checksumok = 'FAIL'

        #if checksum == result[8]:
        #  checksumok = 'PASS'

        data = '{}, {}\n'.format(now, str(result[2]*256+result[3]) #you can add checksumok

    else:
        data = '{}, nodata\n'.format(now) #FAIL

    print(data)

    # Append(追記)モードでファイルを開き、結果を記載して関数処理終了
    file_data = open(saveFileName , "a" )
    file_data.write(data)
    file_data.close()

    # このあとにメール送信を追記したのが消えた、別ファイルのソースを拾ってしまった模様…
    # メール送信はGoogleのSMTPサーバを使用していた
    # 確認できた送信ファイルをslvagedディレクトリに格納

# 当ファイルがトップレベル(=コンソールで実行)で開かれた場合のみ、上記で定義されたセットアップ及びデータ観測関数を実行
if __name__ == '__main__':
    setup()
    while True:
        readdata()