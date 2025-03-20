
from tkinter import BOTH, LEFT, TOP, Button, Entry, Frame, Label, PhotoImage, StringVar, Tk,StringVar,filedialog
from idlelib.tooltip import Hovertip
import sys
import os
from operator import itemgetter
import time
from tkinter import messagebox
from os import listdir
from os.path import isfile, join
from datetime import datetime, date
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import openpyxl
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from urllib.parse import urlparse
import numpy as np
from openpyxl.utils import get_column_letter,column_index_from_string
from datetime import datetime
from pytz import timezone
from zipfile import ZipFile

class functionss():    
    def __init__(self):
        pass

    def driver_check(self,url):
        
        global driver
        
        self.fin_url = url
        
        ck_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")

        fn_ck=os.path.isfile(ck_driver_path)

        if not fn_ck:
            messagebox.showinfo("Driver Message","Chromedriver Not Found")
            sys.exit(0)
        
        try:
            options = Options()            
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument("--disable-popup-blocking")
            prefs ={"profile.password_manager_enabled": False,
                    "credentials_enable_service": False}      
            options.add_experimental_option("prefs",prefs)  
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver_service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=driver_service, options=options)            
            driver.maximize_window()
            driver.get(self.fin_url)
        except Exception as e:
            try:
                options = Options()
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--ignore-ssl-errors')
                options.add_argument("--disable-popup-blocking")                
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                prefs ={"profile.password_manager_enabled": False,
                        "credentials_enable_service": False}      
                options.add_experimental_option("prefs",prefs) 
                driver_path = os.path.abspath('chromedriver.exe')
                driver_service = Service(driver_path)
                driver = webdriver.Chrome(service=driver_service, options=options)                
                driver.maximize_window()
                driver.get(self.fin_url)
            except Exception as e:
                messagebox.showinfo("Driver Problem","Pls Check Your Chrome Driver Version")
                sys.exit(0)

    def text_box(self,xpath,heding,status,key):                
        counter = 0
        while counter < 30:
            try:   
                WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).clear()      
                WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                            
                time.sleep(1)                                           
                WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).send_keys(key)
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:           
            raise e
    
    def text_box2(self,xpath,heding,status,key):                
        counter = 0
        while counter < 30:
            try:                                          
                WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).send_keys(key)                    
                element = WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.send_keys(Keys.TAB)
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:                       
            raise e 

    def text_box1(self,xpath,heding,status,key):                
        counter = 0
        while counter < 30:
            try:  
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.click()                
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.BACKSPACE)                              
                element.send_keys(key)                                           
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:           
            raise e
        
    def text_box_js(self,xpath,heding,status,key):
        counter = 0
        while counter < 30:
            try:   
                WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).clear()  
                ele = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath)))
                driver.execute_script("arguments[0].value = arguments[1]", ele, key)
                driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }))", ele)                                 
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:                      
            raise e

    def click(self,xpath,heding,status):
        counter = 0
        while counter < 30:
            try:             
                WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:                       
            raise e  

    def count(self,xpath,heding,status):
        global rows
        counter = 0
        while counter < 30:
            try:             
                rows=len(WebDriverWait(driver, 0).until(EC.presence_of_all_elements_located((By.XPATH,xpath))))
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:                        
            raise e

    def count_1(self,xpath,heding,status):
        global rows1
        counter = 0
        while counter < 30:
            try:             
                rows1=len(WebDriverWait(driver, 0).until(EC.presence_of_all_elements_located((By.XPATH,xpath))))
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:                        
            raise e   
      
class process():   
    def __init__(self):
        super().__init__()          
        self._fin = None
        self._pass = None

    def curr_process(self,filtered_data,url,usr_nm,pass_word):
        
        global xpath        
        global curr_url

        curr_url=url

        self._fin =  filtered_data
        
        self._fin.loc[:,'Status']=''
        self._fin.loc[:,'Final Status']=''

        self._fin1 = self._fin.head(3).reset_index(drop=True)

        fil = functionss()
        
        fil.driver_check(curr_url)
        
        username=usr_nm
        password=pass_word

        url = f"https://{username}:{password}@secure.tmhp.com/MyAccount/default.aspx?"

        driver.get(url)
                
        try:
            xpath= '/html/body/form/div[3]/div[6]/div/table[1]/tbody/tr/td[1]/fieldset/table/tbody/tr[5]/td/a'
            heding="TexMedConnect"
            status="TexMedConnect Click Not Found"
            fil.click(xpath,heding,status)
        except Exception as e:
            self._pass = 'Medicaid TX - Password Incorrect'
            return
        
 
        for index, row in self._fin1.iterrows():
        # for index, row in self._fin.iterrows():
            try:
                npi = row.iloc[0]
                ctyp = row.iloc[1]
                acc_num=row.iloc[2]
                clt_num=row.iloc[3]
                lst_nm=row.iloc[4]
                fst_nm=row.iloc[5]
                strt=row.iloc[6]
                cty=row.iloc[7]
                st=row.iloc[8]
                zip=row.iloc[9]
                gen=row.iloc[10]
                dob=row.iloc[11]
                id_typ=row.iloc[12]
                ein_ssn=row.iloc[13]
                qulf=row.iloc[14]
                cod=row.iloc[15]
                dos=row.iloc[16]
                pos=row.iloc[17]
                pro_id=row.iloc[18]
                proc=row.iloc[19]
                dig_ref=row.iloc[20]
                qty_unt=row.iloc[21]
                unt_pry=row.iloc[22]
                npi_api=row.iloc[23]
                   
                xpath='/html/body/form/div[5]/div[4]/div/div/table[8]/tbody/tr/td[5]/a'
                heding="Claims Entry"
                status="Claims Entry Click Not Found"
                fil.click(xpath,heding,status)

                xpath='/html/body/form/div[5]/div[6]/div/table[1]/tbody/tr/td[3]/div/span/div[1]/a'
                heding="NPI Dropdown Click"
                status="NPI Dropdown Click Not Found"
                fil.click(xpath,heding,status)
                        
                xpath= "/html/body/form/div[5]/div[6]/div/table[1]/tbody/tr/td[3]/div/span/div[2]/div/table/tbody/tr"
                heding="NPI Tabel Count"
                status="NPI Tabel Count Not Found"                    
                fil.count(xpath,heding,status)
                
                j=1
                while j<rows+1:
                    try:                        
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[5]/div[6]/div/table[1]/tbody/tr/td[3]/div/span/div[2]/div/table/tbody/tr[{}]/td[2]'.format(j)))).text
                        if str(ck).lstrip().rstrip()==str(npi).lstrip().rstrip():                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[5]/div[6]/div/table[1]/tbody/tr/td[3]/div/span/div[2]/div/table/tbody/tr[{}]'.format(j)))).click()                                                
                            break
                    except Exception as e:
                        pass
                    j=j+1

                xpath= "/html/body/form/div[5]/div[6]/div/table[3]/tbody/tr/td[3]/select/option"
                heding="Claim Type Count"
                status="Claim Type Count Not Found"            
                fil.count(xpath,heding,status)
                
                j=1
                while j<rows+1:
                    try:
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[5]/div[6]/div/table[3]/tbody/tr/td[3]/select/option[{}]'.format(j)))).text
                        if str(ck).lower().lstrip().rstrip().replace(' ', '')==str(ctyp).lower().lstrip().rstrip().replace(' ', ''):                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[5]/div[6]/div/table[3]/tbody/tr/td[3]/select/option[{}]'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1

                xpath='/html/body/form/div[5]/div[6]/div/div[2]/input'
                heding="Proceed to Step 2 >> Click"
                status="Proceed to Step 2 >> Click Not Found"
                fil.click(xpath,heding,status)
                
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[1]/table/tbody/tr/td[1]/div[2]/input"
                heding="Account No."
                status="Account No. Not Found"
                key=str(acc_num).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)
                
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[1]/table/tbody/tr/td[3]/div[2]/input"
                heding="Client Number"
                status="Client Number Not Found"
                key=str(clt_num).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[2]/table[1]/tbody/tr/td[1]/div[2]/input"
                heding="Last Name"
                status="Last Name Not Found"
                key=str(lst_nm).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[2]/table[1]/tbody/tr/td[2]/div[2]/input"
                heding="First Name"
                status="First Name Not Found"
                key=str(fst_nm).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[2]/table[2]/tbody/tr/td[1]/div[2]/input"
                heding="Street"
                status="Street Not Found"
                key=str(strt).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[2]/table[2]/tbody/tr/td[2]/div[2]/input"
                heding="City"
                status="City Not Found"
                key=str(cty).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[2]/table[2]/tbody/tr/td[3]/div[2]/select/option"
                heding="State Count"
                status="State Count Not Found"                    
                fil.count(xpath,heding,status)
                
                j=1
                while j<rows+1: 
                    try:                               
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[2]/table[2]/tbody/tr/td[3]/div[2]/select/option[{}]'.format(j)))).text
                        if str(ck).lower().lstrip().rstrip()==str(st).lower().lstrip().rstrip():                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[2]/table[2]/tbody/tr/td[3]/div[2]/select/option[{}]'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[2]/table[2]/tbody/tr/td[4]/div[2]/input"
                heding="ZIP+4"
                status="ZIP+4 Not Found"
                key=str(zip).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[3]/table/tbody/tr/td[1]/div[2]/select/option"
                heding="Gender Count"
                status="Gender  Count Not Found"
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1: 
                    try:                               
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[3]/table/tbody/tr/td[1]/div[2]/select/option[{}]'.format(j)))).text
                        if str(ck).lower().lstrip().rstrip()==str(gen).lower().lstrip().rstrip():                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[3]/table/tbody/tr/td[1]/div[2]/select/option[{}]'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1

                try:
                    original_datetime = datetime.strptime(str(dob), '%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    original_datetime = datetime.strptime(str(dob), '%Y-%m-%d')
                                
                dob1 = original_datetime.strftime('%m/%d/%Y')

                time.sleep(1)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset[3]/table/tbody/tr/td[2]/div[2]/table/tbody/tr/td[1]/table[1]/tbody/tr/td[1]/input"
                heding="Patient Date of Birth"
                status="Patient Date of Birth Not Found"
                key=str(dob1).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                time.sleep(1)

                xpath='/html/body/form/div[5]/div[6]/table[3]/tbody/tr[1]/td[3]/input[2]'
                heding="PATIENT Next"
                status="PATIENT Next Button Not Found"
                fil.click(xpath,heding,status)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset/table[4]/tbody/tr/td[1]/div[2]/select/option"
                heding="ID Type Count"
                status="ID Type Count Not Found"
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1: 
                    try:                               
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset/table[4]/tbody/tr/td[1]/div[2]/select/option[{}]'.format(j)))).text
                        if str(ck).lower().lstrip().rstrip().replace(' ', '')==str(id_typ).lower().lstrip().rstrip().replace(' ', ''):                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset/table[4]/tbody/tr/td[1]/div[2]/select/option[{}]'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td/fieldset/table[4]/tbody/tr/td[2]/div[2]/input"
                heding="EIN/SSN"
                status="EIN/SSN Not Found"
                key=str(ein_ssn).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                xpath='/html/body/form/div[5]/div[6]/table[3]/tbody/tr[1]/td[3]/input[2]'
                heding="PROVIDER Next"
                status="PROVIDER Next Button Not Found"
                fil.click(xpath,heding,status)

                xpath='/html/body/form/div[5]/div[6]/table[3]/tbody/tr[1]/td[3]/input[2]'
                heding="CLAIM Next"
                status="CLAIM Next Button Not Found"
                fil.click(xpath,heding,status)
            
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr/td/div[2]/select/option"
                heding="Qualifier Count"
                status="Qualifier Count Not Found"                    
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1: 
                    try:                               
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr/td/div[2]/select/option[{}]'.format(j)))).text
                        if str(ck).lower().lstrip().rstrip().replace(' ', '')==str(qulf).lower().lstrip().rstrip().replace(' ', ''):                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr/td/div[2]/select/option[{}]'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[2]/div[2]/input"
                heding="Code"
                status="Code Field Not Found"
                key=str(cod).lstrip().rstrip()
                fil.text_box(xpath,heding,status,key)

                xpath='/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[2]/div[2]/img'
                heding="Code Search"
                status="Code Search Not Found"
                fil.click(xpath,heding,status)

                xpath='/html/body/form/div[5]/div[6]/table[3]/tbody/tr[1]/td[3]/input[2]'
                heding="DIAGNOSIS Next"
                status="DIAGNOSIS Next Button Not Found"
                fil.click(xpath,heding,status)            

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[2]/table/tbody/tr[1]/td[3]"
                heding="DOS Click"
                status="DOS Click Not Found"
                fil.click(xpath,heding,status) 

                try:
                    original_datetime = datetime.strptime(str(dos), '%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    original_datetime = datetime.strptime(str(dos), '%Y-%m-%d')
                
                dob2 = original_datetime.strftime('%m/%d/%Y')
                # dob2 = f"{original_datetime.month}/{original_datetime.day}/{original_datetime.year}"

                time.sleep(1)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[1]/div/div[1]/div/table/tbody/tr/td[1]/input"            
                heding="DOS"
                status="DOS Field Not Found"
                key=str(dob2).lstrip().rstrip()
                fil.text_box2(xpath,heding,status,key)            
                
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[1]/div/div[2]/div/div/table/tbody/tr/td[2]/img"
                heding="POS Dropdown Click"
                status="POS Dropdown Click Not Found"
                fil.click(xpath,heding,status)
                
                xpath= "/html/body/form/div[6]/div/ul/li"
                heding="POS Count"
                status="POS Count Not Found"
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1:
                    try:
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[6]/div/ul/li[{}]/a'.format(j)))).text
                        if str(pos).lstrip().rstrip() in str(ck).lstrip().rstrip():                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[6]/div/ul/li[{}]/a'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1            

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[2]/table/tbody/tr[1]/td[5]"
                heding="Proc ID Click"
                status="Proc ID Click Not Found"
                fil.click(xpath,heding,status) 

                xpath="/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[1]/div/div[3]/div/div/table/tbody/tr/td[2]/img"
                heding="Proc ID Dropdown Click"
                status="Proc ID Dropdown Click Not Found"
                fil.click(xpath,heding,status)

                xpath= "/html/body/form/div[7]/div/ul/li"
                heding="Proc ID Count"
                status="Proc ID Count Not Found"
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1: 
                    try:                               
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[7]/div/ul/li[{}]/a'.format(j)))).text
                        if str(pro_id).lstrip().rstrip() in str(ck).lstrip().rstrip():                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[7]/div/ul/li[{}]/a'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1  
                
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[2]/table/tbody/tr[1]/td[6]"
                heding="Proc Click"
                status="Proc Click Not Found"
                fil.click(xpath,heding,status) 
            
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[1]/div/div[4]/input[2]"
                heding="Proc"
                status="Proc Field Not Found"
                key=str(proc).lstrip().rstrip()
                fil.text_box2(xpath,heding,status,key)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[2]/table/tbody/tr[1]/td[14]"
                heding="Diag Ref Click"
                status="Diag Ref Click Not Found"
                fil.click(xpath,heding,status) 
                
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[1]/div/div[12]/div/div/table/tbody/tr/td[2]/img"
                heding="Diag Ref Dropdown Click"
                status="Diag Ref Dropdown Click Not Found"
                fil.click(xpath,heding,status) 

                xpath= "/html/body/form/div[8]/div/ul/li"
                heding="Diag Ref Count"
                status="Diag Ref Count Not Found"                    
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1: 
                    try:                        
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[8]/div/ul/li[{}]/a'.format(j)))).text
                        if str(ck).lstrip().rstrip()==str(dig_ref).lstrip().rstrip():                        
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[8]/div/ul/li[{}]/a'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1
                
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[2]/table/tbody/tr[1]/td[15]"
                heding="Qty/Units Click"
                status="Qty/Units Click Not Found"
                fil.click(xpath,heding,status) 

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[1]/div/div[13]/input[2]"
                heding="Qty/Units"
                status="Qty/Units Field Not Found"
                key=str(qty_unt).lstrip().rstrip()
                fil.text_box2(xpath,heding,status,key)
                                    
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[1]/div/div[14]/input[2]"
                heding="Unit Price"
                status="Unit Price Field Not Found"
                key=str(unt_pry).lstrip().rstrip()
                fil.text_box2(xpath,heding,status,key)

                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[2]/table/tbody/tr[1]/td[18]"
                heding="NPI/API Click"
                status="NPI/API Click Not Found"
                fil.click(xpath,heding,status) 
                
                xpath= "/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[1]/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/table/tbody[2]/tr/td/div[1]/div/div[16]/input[2]"
                heding="NPI/API"
                status="NPI/API Field Not Found"
                key=str(npi_api).lstrip().rstrip()
                fil.text_box2(xpath,heding,status,key)
                
                xpath= "/html/body/div/table/tbody/tr/td/table/tbody/tr/td/font/div/div/table/tbody/tr"
                heding="NPI/API Count"
                status="NPI/API Count Not Found"                    
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1: 
                    try:                               
                        ck=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div/table/tbody/tr/td/table/tbody/tr/td/font/div/div/table/tbody/tr[{}]/td[4]'.format(j)))).text
                        if len(ck.lstrip().rstrip())==10:                                       
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/table/tbody/tr/td/table/tbody/tr/td/font/div/div/table/tbody/tr[{}]/td[4]'.format(j)))).click()                            
                            break
                    except Exception as e:
                        pass
                    j=j+1

                xpath='/html/body/form/div[5]/div[6]/table[3]/tbody/tr[1]/td[3]/input[2]'
                heding="DETAILS Next"
                status="DETAILS Next Button Not Found"
                fil.click(xpath,heding,status)  

                xpath='/html/body/form/div[5]/div[6]/table[2]/tbody/tr/td/div/table[2]/tbody/tr[2]/td/fieldset/table/tbody/tr[2]/td/input'
                heding="Terms And Conditions"
                status="Terms And Conditions Tick Not Found"
                fil.click(xpath,heding,status)  

                # xpath='/html/body/form/div[5]/div[6]/table[3]/tbody/tr[1]/td[1]/div/div/table/tbody/tr[1]/td/input[4]'
                # heding="Submit"
                # status="Submit Button Not Found"
                # fil.click(xpath,heding,status) 

                self._fin1.at[index, 'Status'] = 'Done' 
                
                # counter = 0
                # while counter < 5:
                #     try:                               
                #         sts=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[5]/div[6]/div[1]/p/span/a'))).text                                        
                #         counter1 = 0
                #         while counter1 < 5:
                #             try:
                #                 WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/div[5]/div[6]/div[1]/p/span/a'))).click()          
                #                 fst=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/div[5]/div[6]/div[2]/div[1]'))).text                              
                #                 break
                #             except Exception as e:
                #                 time.sleep(1)
                #                 counter1 += 1
                #         else:
                #             fst='N/A'
                        
                #         self._fin.at[index, 'Status'] = sts 
                        
                #         self._fin.at[index,'Final Status']=fst
                        
                #         break
                #     except Exception as e:
                #         time.sleep(1)
                #         counter += 1
                        
                # else:
                #     self._fin.at[index, 'Status'] = 'Error'                                                 
        
            except Exception as e:
                self._fin1.at[index, 'Status'] = 'Error'

        return self._fin1

class fin_out(process):
    def __init__(self):
        super().__init__()

    def final_process(self,filterdata,url,usr_nm,pass_word):
        
        if not all([url, usr_nm, pass_word]):
            print('URL, Username, or Password is missing')
            return

        self.curr_process(filterdata,url,usr_nm,pass_word)

        if self._pass:
            print(self._pass)
            return
        
        self.fin_data = self._fin1
        
        print(self.fin_data)
        
        print(list(self.fin_data.columns))

        print('Medicaid TX Process Completed...')

        driver.quit()        
           