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
                element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
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
        counter = 0
        while counter < 30:
            try:
                WebDriverWait(driver, 0).until (EC.alert_is_present())
                a=driver.switch_to.alert
                a.accept()
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

    def primary(self,filtered_data,url,usr_nm,pass_word):
        
        global xpath        
        global curr_url
        global heding
        global status

        curr_url=url
        usr_nm=usr_nm
        pass_word=pass_word

        self._fin =  filtered_data

        self._fin.loc[:,'Status']=''
        self._fin.loc[:,'ICN - Number']=''
        self._fin.loc[:,'Paid Amount']=''
        self._fin.loc[:,'Final - Status']=''

        self._fin1 = self._fin.head(3).reset_index(drop=True)

        fil = functionss()
        
        fil.driver_check(curr_url)
        
        xpath='/html/body/div[3]/div/section/div[4]/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/main/article/section[1]/div[1]/div[2]/div[1]/form/div/div/div/div[4]/div[1]/input'
        heding="User Name"
        status="User Name Field Not Found"
        key=str(usr_nm)
        fil.text_box(xpath,heding,status,key)

        xpath='/html/body/div[3]/div/section/div[4]/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/main/article/section[1]/div[1]/div[2]/div[1]/form/div/div/div/div[5]/div[1]/input'
        heding="Password"
        status="Password Field Not Found"
        key=str(pass_word)
        fil.text_box(xpath,heding,status,key)

        xpath='/html/body/div[3]/div/section/div[4]/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/main/article/section[1]/div[1]/div[2]/div[1]/form/div/div/div/div[6]/button'
        heding="Search"
        status="Search Click Not Found"
        fil.click(xpath,heding,status)

        counter = 0
        while counter < 30:            
            try:
                xpath='/html/body/div[3]/div/section/div[4]/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/main/article/section[1]/div[1]/div[2]/div[1]/form/div/div/div/div[3]/div'
                fnd=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath)))
                self._pass = 'Medicaid OH - Username & Password Incorrect'
                return
            except Exception as e:
                try:
                    current_url = driver.current_url
                    if current_url == "https://ohid.ohio.gov/wps/myportal/gov/ohid/":
                        break
                except Exception as e:
                    time.sleep(1)
                    counter += 1
        else:
            self._pass = 'Medicaid OH - Website Not Responce'
            return

        xpath='/html/body/div[3]/section/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/main/article/div/div/div[2]/div[2]/div[4]/div/div/div[2]/div/div[3]/div[2]/a'
        heding="Open App"
        status="Open App Click Not Found"
        fil.click(xpath,heding,status)

        driver.switch_to.window(driver.window_handles[1])           

        counter = 0
        while counter < 30:            
            try:
                tab_name = driver.title
                # print("Current tab title:", tab_name)                
                if "Log In" in tab_name.strip():                    
                    break
            except Exception as e:            
                time.sleep(1)
                counter += 1
        else:
            self._pass = 'Medicaid OH - Website Not Responce'
            return

        xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/div[2]/div[1]/div[2]/div/div/p/span/input'
        heding="Yes, I have read the agreement"
        status="Yes, I have read the agreement Click Not Found"
        fil.click(xpath,heding,status)

        counter = 0
        while counter < 30:            
            try:
                tab_name = driver.title
                # print("Current tab title:", tab_name)                
                if "Provider Management Home" in tab_name.strip():                    
                    break
            except Exception as e:            
                time.sleep(1)
                counter += 1
        else:
            self._pass = 'Medicaid OH - Website Not Responce'
            return

        xpath='/html/body/form/div[6]/div/div/main/div/div[1]/div[3]/div/div[2]/table/tbody/tr/td[1]/a'
        heding="Reg ID"
        status="Reg ID Click Not Found"
        fil.click(xpath,heding,status)

        counter = 0
        while counter < 30:            
            try:
                tab_name = driver.title
                # print("Current tab title:", tab_name)                
                if "Provider Management Details" in tab_name.strip():                    
                    break
            except Exception as e:            
                time.sleep(1)
                counter += 1
        else:
            self._pass = 'Medicaid OH - Website Not Responce'
            return

        xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/table[1]/tbody/tr[5]/td[2]/table/tbody/tr/td[1]'
        heding="Self Service"
        status="Self Service Click Not Found"
        fil.click(xpath,heding,status)
        
        xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/table[1]/tbody/tr[5]/td[2]/table/tbody/tr/td[2]/div/div/div/div[5]/a'
        heding="Claims"
        status="Claims Click Not Found"
        fil.click(xpath,heding,status)

        counter = 0
        while counter < 30:            
            try:
                tab_name = driver.title
                # print("Current tab title:", tab_name)                
                if "Provider Registration Portal" in tab_name.strip():                    
                    break
            except Exception as e:            
                time.sleep(1)
                counter += 1
        else:
            self._pass = 'Medicaid OH - Website Not Responce'
            return
                
        for index, row in self._fin1.iterrows():
            try:
                bil_num = row[0]
                dob = row[1]
                pat_acn = row[2]
                rel_inf=row[3]
                ren_id=row[4]
                dx1=row[5]
                dx2=row[6]
                dx3=row[7]
                dx4=row[8]
                dos=row[9]
                pos=row[10]
                pod_cod=row[11]
                mod1=row[12]
                mod2=row[13]
                mod3=row[14]
                mod4=row[15]
                amt=row[16]
                bil_unt=row[17]
                
                wait = WebDriverWait(driver, 20)
                wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))

                xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/div/ul/li'
                heding="Submit Claim"
                status="Submit Claim Count Not Found"
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1:
                    try:
                        xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/div/ul/li[{}]/a'
                        cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text
                        if cnm.strip()=='Submit Claim':
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j)))).click()
                            break
                    except Exception as e:
                        pass
                    j=j+1
                else:
                    raise e

                wait = WebDriverWait(driver, 20)
                wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))

                xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/div/div[3]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[3]/label'                
                heding="Professional"
                status="Professional Click Not Found"
                fil.click(xpath,heding,status)
                
                wait = WebDriverWait(driver, 20)
                wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))

                xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/div/div[3]/div[2]/div[5]/div[1]/div/div[2]/span/select/option[2]'
                heding="Destination Payer Name"
                status="Destination Payer Name Select Not Found"
                fil.click(xpath,heding,status)
                
                heding="Destination Payer ID"
                status="Destination Payer ID Select Not Found"

                counter = 0
                while counter < 5:
                    try:              
                        xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div/div[2]/span/select/option[2]'                 
                        WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                            
                        break
                    except Exception as e:
                        try:
                            xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div/div[2]/span/select/option'                   
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                            
                            break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1                                                        
                else:
                    raise e
            
                xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/div/div[3]/div[2]/div[5]/div[3]/div/div[2]/span/select/option'
                heding="Destination Payer Responsibility Sequence"
                status="Destination Payer Responsibility Sequence Count Not Found"
                fil.count(xpath,heding,status)
                
                j=1
                while j<rows+1:
                    try:
                        xpath='/html/body/form/div[6]/div[1]/div/main/div/div/div[2]/div/div[3]/div[2]/div[5]/div[3]/div/div[2]/span/select/option[{}]'
                        cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text
                        if cnm.strip()=='Primary':
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j)))).click()                    
                            break
                    except Exception as e:
                        pass
                    j=j+1
                else:
                    raise e

                wait = WebDriverWait(driver, 20)
                wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))
                
                time.sleep(1)
            
                bil_num = str(bil_num)

                if 1 <= len(bil_num.strip()) <= 12:
                    bil_num = bil_num.strip().zfill(12)

                xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div/div[2]/span/input'
                heding="Medical Billing Number"
                status="Medical Billing Number Field Not Found"
                key=str(bil_num)
                fil.text_box(xpath,heding,status,key)

                date_object_1 = datetime.strptime(str(dob), "%Y-%m-%d %H:%M:%S")
                dob3 = date_object_1.strftime("%m/%d/%Y")
                
                xpath= '/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/span/input'
                heding="Date of Birth"
                status="Date of Birth Field Not Found"
                key=dob3
                fil.text_box_key(xpath,heding,status,key)

                xpath= '/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[2]/div/div/div/div/div/div[3]/div[2]/div/div[2]/span/input'
                heding="Patient Control Number"
                status="Patient Control Number Field Not Found"
                key=str(pat_acn)
                fil.text_box_key(xpath,heding,status,key)

                xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div[2]/span/select/option'
                heding="Release of Information"
                status="Release of Information Count Not Found"
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1:
                    try:
                        xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div[2]/span/select/option[{}]'
                        cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text
                        if cnm.strip().lower()==rel_inf.strip().lower():
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j)))).click()
                            break
                    except Exception as e:
                        pass
                    j=j+1
                else:
                    raise e
                
                xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div'
                heding="RENDERING PROVIDER" 
                status="RENDERING PROVIDER Count Not Found"
                fil.count(xpath,heding,status)

                j=1
                while j<rows+1:
                    try:                                     
                        xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[{}]'.format(j)
                        cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text
                        if 'RENDERING PROVIDER' in cnm:

                            total_height = driver.execute_script("return document.body.scrollHeight")
                            scroll_amount = total_height * (10 / 100)
                            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

                            element = WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.XPATH, xpath)))
                            driver.execute_script("arguments[0].click();", element)     
                            
                            time.sleep(2)
                            
                            try:
                                xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[{}]/div/div/div/div/div[2]/div[1]/div/div/span[1]/input'.format(j + 1)
                                element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                                key=str(ren_id)
                                element.send_keys(key)
                            except Exception as e:
                                xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[{}]'.format(j)
                                element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))                           
                                driver.execute_script("arguments[0].click();", element)                             

                                xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[{}]/div/div/div/div/div[2]/div[1]/div/div/span[1]/input'.format(j + 1)                        
                                heding="NPI"
                                status="NPI Field Not Found"
                                key=str(ren_id)
                                fil.text_box_key(xpath,heding,status,key)
                            
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[{}]/div/div/div/div/div[2]/div[1]/div/div/span[1]/span/button'.format(j + 1)
                            heding="NPI Search"
                            status="NPI Search Button Not Found"
                            fil.click(xpath,heding,status)
                            break
                    except Exception as e:
                        pass
                    j=j+1
                else:
                    raise e

                xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[20]/div/div/div[2]/div[2]/div[1]/input'
                heding="NPI 2nd Time"
                status="NPI 2nd Time Field Not Found"
                key=str(ren_id)
                fil.text_box_key(xpath,heding,status,key)
                
                xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[20]/div/div/div[2]/div[2]/div[5]/input'
                heding="NPI 2nd Time Search"
                status="NPI 2nd Time Search Button Not Found"
                fil.click(xpath,heding,status)
                            
                counter = 0
                while counter < 10:
                    try:                                       
                        xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[20]/div/div/div[2]/div[4]/div/div/table/tbody/tr[2]/td[1]/a'                   
                        WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                            
                        break
                    except Exception as e:
                        try:
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[3]/div/div/table/tbody/tr[2]/td[1]/a'                   
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                            
                            break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1                                                        
                else:      
                    raise e
                
                time.sleep(1)

                if pd.isnull(dx1):
                    pass
                else:
                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/input'
                    heding="Diagnosis Code - 01"
                    status="Diagnosis Code - 01 Field Not Found"
                    key=str(dx1)
                    fil.text_box_key(xpath,heding,status,key)
                            
                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/button'
                    heding="Diagnosis Code - 01 Search Button"
                    status="Diagnosis Code - 01 Search Not Found"
                    fil.click(xpath,heding,status)

                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[1]/div[1]/input'
                    heding="Diagnosis Code - 01 2nd Time"
                    status="Diagnosis Code - 01 2nd Time Field Not Found"
                    key=str(dx1)
                    fil.text_box_key(xpath,heding,status,key)

                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[1]/div[4]/input'
                    heding="Diagnosis Code - 01 2nd Time Search Button"
                    status="Diagnosis Code - 01 2nd Time Search Not Found"
                    fil.click(xpath,heding,status)
                
                    counter=0
                    while counter < 10:
                        try:
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[3]/div/div/table/tbody/tr[2]/td[1]/a'
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                            
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[4]/div/input[1]'
                            heding="Diagnosis Code - 01 Add Button"
                            status="Diagnosis Code - 01 Add Button Not Found"
                            fil.click(xpath,heding,status)
                        
                            break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:               
                        raise e         

                if pd.isnull(dx2):
                    pass
                else:                
                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/input'
                    heding="Diagnosis Code - 02"
                    status="Diagnosis Code - 02 Field Not Found"
                    key=str(dx2)
                    fil.text_box_key(xpath,heding,status,key)
                            
                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/button'
                    heding="Diagnosis Code - 02 Search Button"
                    status="Diagnosis Code - 02 Search Not Found"
                    fil.click(xpath,heding,status)

                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[1]/div[1]/input'
                    heding="Diagnosis Code - 02 2nd Time"
                    status="Diagnosis Code - 02 2nd Time Field Not Found"
                    key=str(dx2)
                    fil.text_box_key(xpath,heding,status,key)

                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[1]/div[4]/input'
                    heding="Diagnosis Code - 02 2nd Time Search Button"
                    status="Diagnosis Code - 02 2nd Time Search Not Found"
                    fil.click(xpath,heding,status)
                
                    counter=0
                    while counter < 10:
                        try:
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[3]/div/div/table/tbody/tr[2]/td[1]/a'
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                            
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[4]/div/input[1]'
                            heding="Diagnosis Code - 02 Add Button"
                            status="Diagnosis Code - 02 Add Button Not Found"
                            fil.click(xpath,heding,status)                    
                        
                            break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:               
                        raise e

                if pd.isnull(dx3):
                    pass
                else:                
                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/input'
                    heding="Diagnosis Code - 03"
                    status="Diagnosis Code - 03 Field Not Found"
                    key=str(dx3)
                    fil.text_box_key(xpath,heding,status,key)
                            
                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/button'
                    heding="Diagnosis Code - 03 Search Button"
                    status="Diagnosis Code - 03 Search Not Found"
                    fil.click(xpath,heding,status)

                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[1]/div[1]/input'
                    heding="Diagnosis Code - 03 2nd Time"
                    status="Diagnosis Code - 03 2nd Time Field Not Found"
                    key=str(dx3)
                    fil.text_box_key(xpath,heding,status,key)

                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[1]/div[4]/input'
                    heding="Diagnosis Code - 03 2nd Time Search Button"
                    status="Diagnosis Code - 03 2nd Time Search Not Found"
                    fil.click(xpath,heding,status)

                    counter=0
                    while counter < 10:
                        try:
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[3]/div/div/table/tbody/tr[2]/td[1]/a'
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                                                    
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[4]/div/input[1]'
                            heding="Diagnosis Code - 03 Add Button"
                            status="Diagnosis Code - 03 Add Button Not Found"
                            fil.click(xpath,heding,status)

                            break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:               
                        raise e

                if pd.isnull(dx4):
                    pass
                else:                
                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/input'
                    heding="Diagnosis Code - 04"
                    status="Diagnosis Code - 04 Field Not Found"
                    key=str(dx4)
                    fil.text_box_key(xpath,heding,status,key)
                            
                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/button'
                    heding="Diagnosis Code - 04 Search Button"
                    status="Diagnosis Code - 04 Search Not Found"
                    fil.click(xpath,heding,status)

                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[1]/div[1]/input'
                    heding="Diagnosis Code - 04 2nd Time"
                    status="Diagnosis Code - 04 2nd Time Field Not Found"
                    key=str(dx4)
                    fil.text_box_key(xpath,heding,status,key)

                    xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[1]/div[4]/input'
                    heding="Diagnosis Code - 04 2nd Time Search Button"
                    status="Diagnosis Code - 04 2nd Time Search Not Found"
                    fil.click(xpath,heding,status)
                
                    counter=0
                    while counter < 10:
                        try:
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div/div/div[2]/div/div[3]/div/div/table/tbody/tr[2]/td[1]/a'
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                            
                            xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[19]/div[2]/div/div/div/div[2]/div/div[4]/div/input[1]'
                            heding="Diagnosis Code - 04 Add Button"
                            status="Diagnosis Code - 04 Add Button Not Found"
                            fil.click(xpath,heding,status)
                            
                            break
                        except Exception as e: 
                            time.sleep(1)                   
                            counter += 1
                    else:               
                        raise e
                
                heding="Procedure Code"
                status="Procedure Code Field Not Found"
                key=str(pod_cod)

                counter = 0
                while counter < 15:
                    try:   
                        xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtServiceProcedureCode"]'
                        element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        element.send_keys(key)
                        element.send_keys(Keys.TAB)
                        break
                    # except Exception as e:
                    #     try:
                    #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[5]/div[1]/div[2]/span/input'
                    #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    #         element.send_keys(key)
                    #         element.send_keys(Keys.TAB)
                    #         break
                    except Exception as e:
                        time.sleep(1)
                        counter += 1
                else:
                    raise e   
                    
                heding="Place of Service"
                status="Place of Service Field Not Found"
                key=str(pos)

                counter = 0
                while counter < 15:
                    try:   
                        xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtProfPlaceOfService"]'
                        element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        element.send_keys(key)
                        element.send_keys(Keys.TAB)
                        break
                    # except Exception as e:
                    #     try:
                    #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[5]/div[2]/div[2]/input'
                    #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    #         element.send_keys(key)
                    #         element.send_keys(Keys.TAB)
                    #         break
                    except Exception as e:
                        time.sleep(1)
                        counter += 1
                else:
                    raise e             

                date_object_1 = datetime.strptime(str(dos), "%Y-%m-%d %H:%M:%S")
                dob4 = date_object_1.strftime("%m/%d/%Y")
                
                heding="Date of Service"
                status="Date of Service Field Not Found"
                key=dob4

                counter = 0
                while counter < 15:
                    try:   
                        xpath= '//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtProffdateofservice"]'
                        element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        element.send_keys(key)
                        element.send_keys(Keys.TAB)
                        break
                    # except Exception as e:
                    #     try:
                    #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[6]/div[1]/div[2]/input'
                    #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    #         element.send_keys(key)
                    #         element.send_keys(Keys.TAB)
                    #         break
                    except Exception as e:
                        time.sleep(1)
                        counter += 1
                else:
                    raise e                                 

                if pd.isnull(mod1):
                    pass
                else:                              
                    heding="Modifier 1"
                    status="Modifier 1 Field Not Found"
                    key=str(mod1)

                    counter = 0
                    while counter < 15:
                        try:                          
                            xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtModifier1"]'
                            element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                            element.send_keys(key)
                            element.send_keys(Keys.TAB)
                            break
                        # except Exception as e:
                        #     try:
                        #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[6]/div[2]/div[2]/input[1]'
                        #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        #         element.send_keys(key)
                        #         element.send_keys(Keys.TAB)
                        #         break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:
                        raise e  
                                                                    
                if pd.isnull(mod2):
                    pass
                else:                  
                    heding="Modifier 2"
                    status="Modifier 2 Field Not Found"
                    key=str(mod2)

                    counter = 0
                    while counter < 15:
                        try:   
                            xpath= '//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtModifier2"]'
                            element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                            element.send_keys(key)
                            element.send_keys(Keys.TAB)
                            break
                        # except Exception as e:
                        #     try:
                        #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[6]/div[2]/div[2]/input[2]'
                        #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        #         element.send_keys(key)
                        #         element.send_keys(Keys.TAB)
                        #         break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:
                        raise e                   

                if pd.isnull(mod3):
                    pass
                else:                  
                    heding="Modifier 3"
                    status="Modifier 3 Field Not Found"
                    key=str(mod3)

                    counter = 0
                    while counter < 15:
                        try:   
                            xpath= '//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtModifier3"]'
                            element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                            element.send_keys(key)
                            element.send_keys(Keys.TAB)
                            break
                        # except Exception as e:
                        #     try:
                        #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[6]/div[2]/div[2]/input[3]'
                        #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        #         element.send_keys(key)
                        #         element.send_keys(Keys.TAB)
                        #         break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:
                        raise e                                                                           
                
                if pd.isnull(mod4):
                    pass
                else:                
                    heding="Modifier 4"
                    status="Modifier 4 Field Not Found"
                    key=str(mod4)

                    counter = 0
                    while counter < 15:
                        try:   
                            xpath= '//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtModifier4"]'
                            element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                            element.send_keys(key)
                            element.send_keys(Keys.TAB)
                            break
                        # except Exception as e:
                        #     try:
                        #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[6]/div[2]/div[2]/input[4]'
                        #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        #         element.send_keys(key)
                        #         element.send_keys(Keys.TAB)
                        #         break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:
                        raise e  

                heding="Charges"
                status="Charges Field Not Found"
                key=str(amt)

                counter = 0
                while counter < 15:
                    try:   
                        xpath= '//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtCharges"]'
                        element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        element.send_keys(key)
                        element.send_keys(Keys.TAB)
                        break
                    # except Exception as e:
                    #     try:
                    #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[6]/div[3]/div[2]/input'
                    #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    #         element.send_keys(key)
                    #         element.send_keys(Keys.TAB)
                    #         break
                    except Exception as e:
                        time.sleep(1)
                        counter += 1
                else:
                    raise e            
            
                if pd.isnull(dx1):
                    pass
                else:       
                    heding="Diagnosis Pointer 1"
                    status="Diagnosis Pointer 1 Not Found"

                    counter = 0
                    while counter < 15:
                        try:    
                            xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_ddlDiagnosisPointer1"]/option[2]'         
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                            break
                        # except Exception as e:
                        #     try:
                        #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[7]/div[2]/div[2]/select[1]/option[2]'         
                        #         WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                        #         break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:
                        raise e                      
                    
                if pd.isnull(dx2):
                    pass
                else:    
                    heding="Diagnosis Pointer 2"
                    status="Diagnosis Pointer 2 Not Found"

                    counter = 0
                    while counter < 15:
                        try:    
                            xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_ddlDiagnosisPointer2"]/option[2]'         
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                            break
                        # except Exception as e:
                        #     try:
                        #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[7]/div[2]/div[2]/select[2]/option[2]'         
                        #         WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                        #         break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:
                        raise e                   
                
                if pd.isnull(dx3):
                    pass
                else:    
                    heding="Diagnosis Pointer 3"
                    status="Diagnosis Pointer 3 Not Found"

                    counter = 0
                    while counter < 15:
                        try:    
                            xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_ddlDiagnosisPointer3"]/option[2]'         
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                            break
                        # except Exception as e:
                        #     try:
                        #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[7]/div[2]/div[2]/select[3]/option[2]'         
                        #         WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
                        #         break
                        except Exception as e:
                            time.sleep(1)
                            counter += 1
                    else:
                        raise e                                            

                heding="Billed Units"
                status="Billed Units Field Not Found"
                key=str(bil_unt)

                counter = 0
                while counter < 15:
                    try:    
                        xpath= '//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_txtBilledUnits"]'         
                        element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                        element.send_keys(key)
                        element.send_keys(Keys.TAB)
                        break
                    # except Exception as e:
                    #     try:
                    #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[7]/div[3]/div[2]/input'         
                    #         element = WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    #         element.send_keys(key)
                    #         element.send_keys(Keys.TAB)
                    #         break
                    except Exception as e:
                        time.sleep(1)
                        counter += 1
                else:
                    raise e
                    
                heding="Unit of Measurement" 
                status="Unit of Measurement Count Not Found"

                counter = 0
                while counter < 15:
                    try:      
                        xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_ddlUnitsOfMeasurement"]/option'       
                        rows_2=len(WebDriverWait(driver, 0).until(EC.presence_of_all_elements_located((By.XPATH,xpath))))                    
                        break
                    # except Exception as e:
                    #     try:
                    #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[8]/div[3]/div[2]/select/option'       
                    #         rows_2=len(WebDriverWait(driver, 0).until(EC.presence_of_all_elements_located((By.XPATH,xpath))))                    
                    #         break
                    except Exception as e:
                        time.sleep(1)
                        counter += 1
                else:
                    raise e 

                j=1
                while j<rows_2+1:
                    try:
                        xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_ddlUnitsOfMeasurement"]/option[{}]'
                        cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text
                        if cnm.strip()=='UN':
                            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j)))).click()                                                                                            
                            break
                    # except Exception as e:
                    #     try:
                    #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[8]/div[3]/div[2]/select/option[{}]'
                    #         cnm=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath.format(j)))).text
                    #         if cnm.strip()=='UN':
                    #             WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath.format(j)))).click()                                                                                            
                    #             break
                    except Exception as e:
                        pass
                    j=j+1
                else:
                    raise e
                
                total_height = driver.execute_script("return document.body.scrollHeight")
                scroll_amount = total_height * (5 / 100)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

                time.sleep(1)

                heding="SERVICE DETAILS"
                status="SERVICE DETAILS Add Button Not Found"

                counter = 0
                while counter < 15:
                    try:      
                        xpath='//*[@id="ctl00_MainContent_uc5SubmitClaim_ProfessionalServiceLineDetails_ProfInfoAdd"]'       
                        WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()          
                        break
                    # except Exception as e:
                    #     try:
                    #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[27]/div[2]/div/div[1]/div[1]/div[3]/div[11]/div[3]/input[1]'       
                    #         WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                
                    #         break
                    except Exception as e:
                        time.sleep(1)
                        counter += 1
                else:
                    raise e            

                time.sleep(2)

                wait = WebDriverWait(driver, 20)
                wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))
                
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # /html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[54]/div/div/div/div[2]/input[2]
                # xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[52]/div/div/div/div[2]/input[2]'
                # heding="Submit"
                # status="Submit Button Not Found"
                # click(xpath,heding,status)
                
                self._fin1.at[index, 'Final - Status'] = 'Done' 

                # counter=0
                # while counter < 5:
                #     try:                            
                #         xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[52]/div/div/div/div[2]/input[2]"
                #         WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                                                                                            
                #         break                   
                #     except Exception as e:
                #         try:
                #             xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[54]/div/div/div/div[2]/input[2]"
                #             WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                                                                                            
                #             break
                #         except Exception as e:
                #             time.sleep(1)
                #             counter += 1
                # else:
                #     heding="Submit"
                #     status="Submit Button Not Found"
                #     messagebox.showinfo(heding,status)
                #     sys.exit(0)

                # wait = WebDriverWait(driver, 20)
                # wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))
                
                # xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[4]/div[1]/table/tbody/tr/td[1]'
                # st=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath))).text

                # xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[4]/div[3]/input'
                # heding="Success"
                # status="Success OK Button Not Found"
                # fil.click(xpath,heding,status)            

                # counter=0
                # while counter < 8:
                #     try:                                                            
                #         xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[2]/div[2]/div/div[1]/input"
                #         cs=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath)))  
                #         cs = cs.get_attribute("value")                    
                        
                #         xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[2]/div[2]/div/div[2]/input"
                #         icn=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath)))  
                #         icn = icn.get_attribute("value")                     

                #         xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[2]/div[2]/div/div[3]/input"
                #         fin_amt=WebDriverWait(driver, 0).until(EC.visibility_of_element_located((By.XPATH,xpath)))  
                #         fin_amt = fin_amt.get_attribute("value")                    

                #         self._fin.at[index, 'Status'] = cs 
                #         self._fin.at[index, 'ICN - Number'] = icn 
                #         self._fin.at[index, 'Paid Amount'] = fin_amt 
                #         self._fin.at[index, 'Final - Status'] = 'Done' 

                            # self._fin.loc[:,'Status']=''
                            # self._fin.loc[:,'ICN - Number']=''
                            # self._fin.loc[:,'Paid Amount']=''
                            # self._fin.loc[:,'Final - Status']=''

                #         break
                #     except Exception as e:
                #         time.sleep(1)
                #         counter += 1
                # else:
                #     self._fin.at[index, 'Status'] = 'Error'  
                                        
                # if st=='Failed':                         
                #     try:
                #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[52]/div/div/div/div[2]/input[3]'
                #         WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click() 
                #     except Exception as e:
                #         xpath='/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[54]/div/div/div/div[2]/input[3]'
                #         WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click() 
                # else:            
                #     counter=0
                #     while counter < 5:
                #         try:    
                #             xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[52]/div/div/div/div[2]/input[2]"
                #             WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                                                                                            
                #             break                   
                #         except Exception as e:
                #             try:
                #                 xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[54]/div/div/div/div[2]/input[2]"
                #                 WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                                                                                            
                #                 break   
                #             except Exception as e:
                #                 try:
                #                     xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[52]/div/div/div/div[2]/input"
                #                     WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                                                                                            
                #                     break
                #                 except Exception as e:
                #                     try:
                #                         xpath= "/html/body/form/div[6]/div/div/main/div/div/div[2]/div/div[3]/div[2]/div[6]/div[1]/div[1]/div[54]/div/div/div/div[2]/input"
                #                         WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()                                                                                            
                #                         break
                #                     except Exception as e:
                #                         time.sleep(1)
                #                         counter += 1
                #     else:
                #         heding="Cancel"
                #         status="Cancel Button Not Found"
                #         messagebox.showinfo(heding,status)
                #         sys.exit(0)

                fil.Alert()                    
            except Exception as e:
                self._fin1.at[index, 'Final - Status'] = 'Error'
                                
class fin_out_OH(process):
    def __init__(self):
        super().__init__()

    def final_process_OH(self,filterdata,url,usr_nm,pass_word):
        
        if not all([url, usr_nm, pass_word]):
            print('URL, Username, or Password is missing')
            return

        self.primary(filterdata,url,usr_nm,pass_word)

        if self._pass:
            print(self._pass)
            return
        
        self.fin_data = self._fin1
        
        print(self.fin_data)
        
        print(list(self.fin_data.columns))

        print('Medicaid OH Process Completed...')

        driver.quit()     


   