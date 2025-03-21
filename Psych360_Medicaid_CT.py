from tkinter import BOTH, LEFT, TOP, Button, Entry, Frame, Label, PhotoImage, StringVar, Tk,Radiobutton,StringVar,IntVar,filedialog
from idlelib.tooltip import Hovertip
from tkinter import messagebox
import sys
import os
import warnings
from datetime import datetime, date
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import openpyxl
import time
import pandas as pd
from openpyxl import load_workbook
from urllib.parse import urlparse
import warnings
import numpy as np
import requests
from zipfile import ZipFile
from openpyxl.utils import get_column_letter,column_index_from_string
warnings.filterwarnings("ignore")

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
                WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).send_keys(key)
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:
            raise e  
    
    def text_box_key(self,xpath,heding,status,key):                
        counter = 0
        while counter < 30:
            try:   
                element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                element.send_keys(key)
                element.send_keys(Keys.TAB)
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
        global rows_1
        counter = 0
        while counter < 30:
            try:             
                rows_1=len(WebDriverWait(driver, 0).until(EC.presence_of_all_elements_located((By.XPATH,xpath))))                    
                break
            except Exception as e:
                time.sleep(1)
                counter += 1
        else:
            raise e 

    def Alert(self):            
        try:             
            WebDriverWait(driver, 1).until (EC.alert_is_present())
            a=driver.switch_to.alert
            a.accept()                
        except Exception as e:
            pass

class primary_CT():
    def __init__(self):
        super().__init__()    
        self._fin = None
        self._pass = None

    def primary_process_CT(self,filtered_data,url,usr_nm,pass_word):        
        global xpath        
        global curr_url
        global heding
        global status
        global j
        global i       
        
        curr_url=url
        usr_nm=usr_nm
        pass_word=pass_word

        self._fin =  filtered_data

        self._fin.loc[:,'Claim Status']=''
        self._fin.loc[:,'Code1']=''
        self._fin.loc[:,'Description1']=''
        self._fin.loc[:,'Code2']=''
        self._fin.loc[:,'Description2']=''
        self._fin.loc[:,'Code3']=''
        self._fin.loc[:,'Description3']=''
        self._fin.loc[:,'Code4']=''
        self._fin.loc[:,'Description4']=''
        self._fin.loc[:,'Code5']=''
        self._fin.loc[:,'Description5']=''
        self._fin.loc[:,'Claim Number']=''
        self._fin.loc[:,'Claim Paid']=''
        self._fin.loc[:,'Final Status']=''

        # self._fin['AVRS ID#'] = pd.to_numeric(self._fin['AVRS ID#'], errors='coerce').astype('float').astype('Int64')

        self._fin1 = self._fin.head(3).reset_index(drop=True)

        fil = functionss()
    
        fil.driver_check(curr_url)

        xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[3]/div[1]/div/div/div/fieldset/table/tbody/tr[1]/td[2]/input'
        heding="User ID"
        status="User ID Field Not Found"
        key=usr_nm
        fil.text_box(xpath,heding,status,key)
        
        xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[3]/div[1]/div/div/div/fieldset/table/tbody/tr[2]/td[2]/input'
        heding="Password"
        status="Password Field Not Found"
        key=pass_word
        fil.text_box(xpath,heding,status,key)

        xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[3]/div[1]/div/div/div/fieldset/table/tbody/tr[3]/td/a"
        heding="Login"        
        status="Login Button Not Found"
        fil.click(xpath,heding,status)
        
        page_title = driver.title

        time.sleep(1)

        if page_title.lstrip().rstrip()=='Secure Site':                               
            self._pass = 'Medicaid CT - Username & Password Incorrect'
            return                                     
                                    
        for index, row in self._fin1.iterrows():                          
            try:
                c_id = row[0]                 
                p_acn = row[1]            
                dx = row[2]                 
                f_dos=row[3]                                    
                pro=row[4]
                mod=row[5]
                ftc=row[6]
                amt=row[7]
                ren_phy=row[8]
                mp_dt=row[9]
                mc_amt=row[10]
                mp_amt=row[11]
                md_amt=row[12]
                mcins_amt=row[13]
                avrs=row[14]

                # avrs_1 = '00' + str(avrs)
                
                if 1 <= len(avrs.strip()) <= 9:
                    avrs = avrs.strip().zfill(9)

                wait = WebDriverWait(driver, 20)
                wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))
                
                xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/div[1]/ul/li"
                heding="Account"
                status="Account Tab Count Not Found"        
                fil.count(xpath,heding,status)

                xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/div[1]/ul/li[{}]"

                j=1
                while j<rows+1:                                
                    cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text            
                    if cnm.lstrip().rstrip()=="Account":
                        
                        time.sleep(1)

                        element=WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j))))
                        actions = ActionChains(driver)
                        actions.move_to_element(element).perform()  

                        xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/div[1]/ul/li[{}]/ul/li".format(j)
                        heding="Account Count"
                        status="Sub Account Count Not Found"        
                        fil.count_1(xpath,heding,status)                
                            
                        i=1
                        while i<rows_1+1:                                       
                            xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/div[1]/ul/li[{}]/ul/li[{}]"
                            element_7=WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j,i))))
                            actions = ActionChains(driver)
                            actions.move_to_element(element_7).perform()  
                            element_text = element_7.text                    
                            if element_text.lstrip().rstrip()=="Switch Provider":
                                WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j,i)))).click()  
                                break                       
                            i=i+1                                                              
                        break
                    j=j+1                            
                
                fil.Alert()

                try:
                    element_5=WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr')))

                    xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr"
                    heding="Switch Provider Table"
                    status="Switch Provider Table Count Not Found"        
                    fil.count(xpath,heding,status)  
                    
                    j=2
                    while j<rows+1:     
                        xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr[{}]/td[3]"    
                        cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text
                        if cnm.lstrip().rstrip()==avrs.lstrip().rstrip():
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j)))).click()  

                            xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/span[2]/table/tbody/tr/td/table/tbody/tr[1]/td[5]/table/tbody/tr/td/a"
                            heding="Switch"
                            status="Switch Button Not Found"
                            fil.click(xpath,heding,status)

                            fil.Alert()

                            break
                        j=j+1
                except Exception as e:
                    pass

                xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/div[1]/ul/li"
                heding="Claims"
                status="Claims Tab Count Not Found"        
                fil.count(xpath,heding,status)

                xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/div[1]/ul/li[{}]"

                j=1            
                while j<rows+1:                                
                    cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text            
                    if cnm.lstrip().rstrip()=="Claims":
                        
                        time.sleep(1)

                        element=WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j))))
                        actions = ActionChains(driver)
                        actions.move_to_element(element).perform()  

                        xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/div[1]/ul/li[{}]/ul/li".format(j)
                        heding="Sub Claims Count"
                        status="Sub Claims Count Not Found"    
                        fil.count_1(xpath,heding,status)                
                            
                        i=1
                        while i<rows_1+1:                                       
                            xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[2]/tbody/tr/td/div[1]/ul/li[{}]/ul/li[{}]"
                            element_7=WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j,i))))
                            actions = ActionChains(driver)
                            actions.move_to_element(element_7).perform()  
                            element_text = element_7.text                    
                            if element_text.lstrip().rstrip()=="Professional":
                                WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j,i)))).click()  
                                break                       
                            i=i+1                                                              
                        break
                    j=j+1       
                
                c_id = str(c_id)

                if 1 <= len(c_id.strip()) <= 9:
                    c_id = c_id.strip().zfill(9)

                fil.Alert()

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/span/table/tbody/tr[1]/td/table/tbody/tr[4]/td[2]/input'
                heding="Client ID"
                status="Client ID Field Not Found"
                key=c_id
                fil.text_box(xpath,heding,status,key)

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/span/table/tbody/tr[1]/td/table/tbody/tr[8]/td[2]/input'
                heding="Patient Account"
                status="Patient Account Number Field Not Found"
                key=p_acn
                fil.text_box(xpath,heding,status,key)

                xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/span/table/tbody/tr[1]/td/table/tbody/tr[10]/td[4]/select/option"
                heding="Medicare Crossover"
                status="Medicare Crossover Count Not Found"        
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1:                                       
                    xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/span/table/tbody/tr[1]/td/table/tbody/tr[10]/td[4]/select/option[{}]"
                    cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text
                    if cnm.lstrip().rstrip()=='Yes':
                        WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j)))).click()  
                        break                       
                    j=j+1
                
                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[1]/span/table/tbody/tr/td/table/tbody/tr[2]/td[2]/span/input'
                heding="Diagnosis"
                status="Principal Field Not Found"
                key=dx
                fil.text_box(xpath,heding,status,key)

                date_object_1 = datetime.strptime(str(f_dos), "%Y-%m-%d %H:%M:%S")
                dob3 = date_object_1.strftime("%m/%d/%Y")

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input'
                heding="Detail"
                status="From DOS Field Not Found"
                key=dob3
                fil.text_box(xpath,heding,status,key)

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[4]/td[2]/span/input'
                heding="Detail"
                status="Procedure Field Not Found"
                key=pro
                fil.text_box(xpath,heding,status,key)

                if pd.isnull(mod):
                    mod = str(mod)
                else: 
                    xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[5]/td[2]/span[1]/input'
                    heding="Detail"
                    status="Modifiers Field Not Found"
                    key=mod
                    fil.text_box(xpath,heding,status,key)

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[8]/td[2]/span/input'
                heding="Detail"
                status="Facility Type Code Field Not Found"
                key=ftc
                fil.text_box(xpath,heding,status,key)
                
                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[9]/td[2]/input'
                heding="Detail"
                status="Charges Field Not Found"
                key=amt
                fil.text_box(xpath,heding,status,key)

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[10]/td[2]/input[1]'
                heding="Detail"
                status="Rendering Physician Field Not Found"
                key=ren_phy
                fil.text_box(xpath,heding,status,key)
                
                date_object_1 = datetime.strptime(str(mp_dt), "%Y-%m-%d %H:%M:%S")
                dob3 = date_object_1.strftime("%m/%d/%Y")

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[8]/td[4]/input'
                heding="Detail"
                status="Medicare Paid Date Field Not Found"
                key=dob3
                fil.text_box(xpath,heding,status,key)

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[9]/td[4]/input'
                heding="Detail"
                status="Medicare Calc Allowed Amt Field Not Found"
                key=mc_amt
                fil.text_box(xpath,heding,status,key)

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[10]/td[4]/input'
                heding="Detail"
                status="Medicare Paid Amount Field Not Found"
                key=mp_amt
                fil.text_box(xpath,heding,status,key)

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[11]/td[4]/input'
                heding="Detail"
                status="Medicare Deductible Amount Field Not Found"
                key=md_amt
                fil.text_box(xpath,heding,status,key)

                xpath= '/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[3]/span/table/tbody/tr/td/table/tbody/tr[12]/td[4]/input'
                heding="Detail"
                status="Medicare Coinsurance Amount Field Not Found"
                key=mcins_amt
                fil.text_box(xpath,heding,status,key)
                
                self._fin1.at[index, 'Final Status'] = 'Done'  

                # xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/span[2]/table/tbody/tr/td[3]/table/tbody/tr/td[1]/a"
                # heding="Submit"
                # status="Submit Button Not Found"
                # fil.click(xpath,heding,status)

                # wait = WebDriverWait(driver, 20)
                # wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))

                # xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/span/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/input"   
                # cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath)))
                # cnm = cnm.get_attribute("value") 
                
                # if cnm.lstrip().rstrip()=='Not Submitted yet':                    
                #     self._fin1.at[index, 'Final Status'] = 'Error'  
                # else:      
                                                    
                #     xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/span/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/input"
                #     cs=WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,xpath)))  
                #     cs = cs.get_attribute("value") 
                #     self._fin1.at[index, 'Claim Status'] = cs

                #     if cs=='DENIED':
                #         try:
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[3]/td[2]"                                 
                #             cd1=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text
                            
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[3]/td[3]"                                 
                #             dec1=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text
                            
                #             self._fin1.at[index, 'Code1'] = cd1
                #             self._fin1.at[index, 'Description1'] = dec1
                #         except Exception as e:
                #             pass
                        
                #         try:
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[4]/td[2]"                                 
                #             cd2=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text
                            
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[4]/td[3]"                                 
                #             dec2=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text

                #             self._fin1.at[index, 'Code2'] = cd2
                #             self._fin1.at[index, 'Description2'] = dec2
                #         except Exception as e:
                #             pass
                        
                #         try:
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[5]/td[2]"                                 
                #             cd3=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text
                            
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[5]/td[3]"                                 
                #             dec3=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text

                #             self._fin1.at[index, 'Code3'] = cd3
                #             self._fin1.at[index, 'Description3'] = dec3
                #         except Exception as e:
                #             pass
                        
                #         try:
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[6]/td[2]"                                 
                #             cd4=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text
                            
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[6]/td[3]"                                 
                #             dec4=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text

                #             self._fin1.at[index, 'Code4'] = cd4
                #             self._fin1.at[index, 'Description4'] = dec4
                #         except Exception as e:
                #             pass

                #         try:
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[7]/td[2]"                                 
                #             cd5=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text
                            
                #             xpath="/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/table/tbody/tr[7]/td[3]"                                 
                #             dec5=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text

                #             self._fin1.at[index, 'Code5'] = cd5
                #             self._fin1.at[index, 'Description5'] = dec5
                #         except Exception as e:
                #             pass

                #     xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/span/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input"
                #     c_icn=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j))))
                #     c_icn = c_icn.get_attribute("value") 
                #     self._fin1.at[index, 'Claim Number'] = c_icn

                #     xpath= "/html/body/form/div[3]/table/tbody/tr[1]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/div/div[5]/span/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[5]/td[2]/input"
                #     p_amt=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j))))
                #     p_amt = p_amt.get_attribute("value") 
                #     self._fin1.at[index, 'Claim Paid'] = p_amt
                                                                                                                                                                            
                #     self._fin1.at[index, 'Final Status'] = 'Done'                
            except Exception as e:
                self._fin1.at[index, 'Final Status'] = 'Error'                                      
                                                     
class fin_out_CT(primary_CT):
    def __init__(self):
        super().__init__()

    def final_process_CT(self,filterdata,url,usr_nm,pass_word):
        
        if not all([url, usr_nm, pass_word]):
            print('URL, Username, or Password is missing')
            return

        self.primary_process_CT(filterdata,url,usr_nm,pass_word)

        if self._pass:
            print(self._pass)
            return
        
        self.fin_data = self._fin1
        
        print(self.fin_data)
        
        print(list(self.fin_data.columns))

        print('Medicaid CT Process Completed...')

        driver.quit() 

   