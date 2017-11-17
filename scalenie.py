import csv
import os
import json
from dbfread import DBF

final_out = []
year_values = []
order_list_remarks = []
year = 2017

# Tablica z folderami do odczytania
foldArr = ['K_999985','K_999986','K_999987','K_999988','K_999989','K_999990','K_999991']


def openBase(folder):
    global year
    year -= 1
    counter = 0
    path = os.path.join(r'C:\Users\Jan Sratatam\Desktop\baza\n', folder,r'KARTZSPE.csv')
    print(path)
    # Otwiera KARTZARO.DBF ,żeby pobrać z niego dane do ZUWAGI,RODZ_NACZ
    tablePath = os.path.join(r'C:\Users\Jan Sratatam\Desktop\baza\n', folder, r'KARTZARO.DBF')
    print ( tablePath )
    table =  DBF(tablePath ,encoding='latin10')
    for record in table:
        order_list_remarks.append(record)
        counter += 1

    # Pobiera z pliku listę nagłówków, wg których będzie tworzona lista

    file =  open ( r"C:\Users\Jan Sratatam\Desktop\baza\KARTZSPE_dane.txt", 'r')
  
    headers_val = file.read().rstrip().split(',')


    with open(path , newline='')as csvfile:

        reader = csv.reader(csvfile)
        header = next(reader)
        text = (', '.join(header))

        # Tablica z nagłówkiem z nazwami pól
        header_arr = text.split(';')

        # Przechowuje wszystkie zlecenia
        orders_arr = []
        # Przechowuje aktualne zlecenie

        curr_item = {}
        num = 0
        for element in reader:
            item_text = (', '.join(element))
            # Tablica zleceń
            item_arr = item_text.split(';')

            # Tymczasowy słownik ze zleceniem i warościami nagłówka
            num = 0
            for num in range(0,len(header_arr)):
                curr_item[header_arr[num]] = item_arr[num]
                num += 1
            curr_item['RODZ_NACZ'] = ""
            orders_arr.append(curr_item)
            curr_item = {}

        for o_a in orders_arr:
            for o_l_r in order_list_remarks:
                if int(o_a['NR_ZWYJ']) == int(o_l_r['NR_ZWYJ']):
                    o_a['NAZ_TOWARU'] = o_l_r['NAZ_TOWARU']
                    o_a['CCIE_TOWAR'] = o_l_r['CCIE_TOWAR']
                    o_a['ZUWAGI'] = o_l_r['ZUWAGI']
                    o_a['RODZ_NACZ'] = o_l_r['RODZ_NACZ']


        c_i = {}
        # Formatuje każdy obiekt i dodaj dodatkow wartości do obiektu
        for res in orders_arr:
            for h_v in headers_val:
                c_i[h_v] = res[h_v]
            c_i['SHOW_STATUS'] = "false"
            c_i['YEAR'] = year
            c_i['CENA_JM1'] = c_i['CENA_JM1'].replace ( " ", "" ).split ( "," )[0]
            c_i['STFR_PRZE'] = c_i['STFR_PRZE'].replace ( " ", "" ).split ( "," )[0]
            final_out.append(c_i)
            c_i = {}



# Funkcja wyjonywana dla wszystkich katalogów z foldArr
for val in foldArr:
    openBase(val)



# Zapisuje dane z final_out do formatu JSON
with open ( r"C:\Users\Jan Sratatam\Desktop\1.txt", 'w' ) as f:
    json.dump ( final_out, f )
