import requests
import json
import sqlite3 as sql
import pprint
conn = sql.connect("yolculukgecmisim.db") #sql baglantin

cursor = conn.cursor()

def satinalmagecmisi() :
 print("Mevcut biletler : ")

 cursor.execute("SELECT *FROM BILETLER")

 mevcut = cursor.fetchall()

 pprint.pprint(mevcut)
 print("************************************************")



satinalmagecmisi()


cursor.execute("CREATE TABLE IF NOT EXISTS BILETLER( isim TEXT,koltuk TEXT,ucus_no TEXT,ucus_saati TEXT,ucus_tarihi TEXT,havalimani TEXT)")

url = 'https://api.schiphol.nl/public-flights/flights?flightDirection=D&includedelays=false&page=1&sort=%2BscheduleTime&fromScheduleDate=2022-05-10&toScheduleDate=2022-05-12'



cevap = requests.get(url, headers = {"app_id" : "d2d9b7c6" , "app_key" : "4199d6efb553a75906721ed6c76cf512","ResourceVersion" : "v4","Accept": "application/json" })

if cevap.status_code ==200: #protokol surecinin dogru olduğuna dair cevap kodu
    veri  = json.loads(cevap.text) #json -->dict

else:
    print("HATA! Request islemi basarısız oldu ")


print("Ucus planlamak icin ; ")

havalimanı_kodu = input("Havalimani kodunu giriniz : ")

print(" ")
for x in range(20):  #gidilen havalimanları
 if veri["flights"][x]["route"]['destinations'][0] ==havalimanı_kodu:
  print("Secim numarasi : ",x,veri["flights"][x]["route"]['destinations'][0], " : ","Ucus numarasi ",veri["flights"][x]['flightNumber'],"Tarih : ",veri["flights"][x]['scheduleDate'],"Saat : ",veri["flights"][x]['scheduleTime'])

x = input("secim numarasını giriniz : ")
print(" ")

yolcu_ismi = input("Yolcu ismini giriniz")
koltuk = input("Koltuk seciminizi giriniz : ")


print(" ")
x=int(x)

cursor.execute("INSERT INTO BILETLER(isim,koltuk,ucus_no,ucus_saati,ucus_tarihi,havalimani)VALUES(?,?,?,?,?,?)",(yolcu_ismi,koltuk,veri["flights"][x]['flightNumber'],veri["flights"][x]['scheduleTime'],veri["flights"][x]['scheduleDate'],veri["flights"][x]["route"]['destinations'][0]))

print("Secim numarasi : ", x, veri["flights"][x]["route"]['destinations'][0], " : ", "Ucus numarasi ",
      veri["flights"][x]['flightNumber'], "Tarih : ", veri["flights"][x]['scheduleDate'], "Saat : ",
      veri["flights"][x]['scheduleTime'])


print("Ucusunuz secildi ve kaydedildi.")
print(" ")

satinalmagecmisi()

conn.commit()  #database e işle
conn.close()   #baglantiyi sonlandir