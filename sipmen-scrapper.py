from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import lxml

index_url='https://sipmen.bps.go.id/regsosek/sipmen-terima-kab/index'
first_page=index_url+'?halaman=1&search='
login_url='https://sipmen.bps.go.id/regsosek/login'

# user login credential
email='emailmu@gmail.com'
password="password123"

driver = webdriver.Chrome('./chromedriver')
driver.get(first_page)

time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# simulasi login
if(driver.current_url==login_url):
    wait = WebDriverWait(driver, 1)
    wait.until(EC.element_to_be_clickable((By.ID, "email"))).send_keys(email)
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Sign In']"))).click()
    
time.sleep(2)

# halaman index/ halaman pertama
if(driver.current_url==first_page):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    soup_table = soup.find("table")
    
    table = pd.read_html(str(soup_table), converters ={x:str for x in ['KODE WILAYAH', 'NO SLS']})[0]
    # skip baris pertama karna bernilai NaN
    table = table.iloc[1:, :]

    #halaman kedua dst
    dataIsAvailable = True
    page=2
    while(dataIsAvailable):

        url = index_url+'?halaman='+str(page)+'&search='

        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        soup_table = soup.find("table")
        tempTable = pd.read_html(str(soup_table), converters ={x:str for x in ['KODE WILAYAH', 'NO SLS']})[0]
        # kalau halaman terakhir, maka cuma ada satu row, nilainya 'tidak ditemukan'
        print(len(tempTable.index))
        if(len(tempTable.index)<=1):
            dataIsAvailable=False
            # table['KODE WILAYAH'].astype(str)
            # table['NO SLS'].astype(str)
            table.to_csv('sipmen_penerimaan_dari_koseka')
        else:
            tempTable = tempTable.iloc[1:, : ]
            table = pd.concat([table, tempTable]).reset_index(drop=True)
        page=page+1
        

driver.close()
