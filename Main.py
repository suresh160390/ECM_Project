from dotenv import load_dotenv
from Medicaid_TX import *
from Psych360_Medicaid_OH import *
from Psych360_Medicaid_CT import *
import traceback
import pandas as pd
import pyodbc


class login_db():
    def __init__(self):
        
        self.__df=None        
        self.__tph=None
        self._err=None

        load_dotenv()      

        self.__server = os.getenv('db_loc')
        self.__database = os.getenv('db_name')
        self.__username = os.getenv('user_name')
        self.__password = os.getenv('pass_word')
        self.__driver = os.getenv('driver')

        self.__connection_string = f"DRIVER={{{self.__driver}}};SERVER={self.__server};DATABASE={self.__database};UID={self.__username};PWD={self.__password}"

    def db_data(self):
        try:
            acc=43
            conn = pyodbc.connect(self.__connection_string)
            cursor = conn.cursor()

            cursor.execute("EXEC rules_getOnlineSubmissionClaims @accountId = ?",acc)
            rows = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            
            df1 = pd.DataFrame.from_records(rows, columns=columns)
            
            self.__tph=df1
            
            cursor.close()
            conn.close()

        except Exception as e:
            self._err = 'Data Database Connection Error'
            return None
            
        return self.__tph
    
    def db_login(self):
        try:           
            conn = pyodbc.connect(self.__connection_string)
            cursor = conn.cursor()

            cursor.execute("select * from rules.MCDConfiguration")
            rows = cursor.fetchall()

            columns = [col[0] for col in cursor.description]
            
            df1 = pd.DataFrame.from_records(rows, columns=columns)
            
            self.__df=df1
            
            cursor.close()
            conn.close()

        except Exception as e:
            self._err = 'Login Database Connection Error'
            return None
            
        return self.__df

class start(login_db):
    def __init__(self):
        super().__init__()
        self._fin=None
        self._tph=None
        self._err = None

    def main_process(self):        
        try:
            self._fin = self.db_login()
            
            if self._err:
                print(self._err)
                return
            
            self._tph = self.db_data()
                       
            if self._err:
                print(self._err)
                return
                        
            for index, row in self._fin.iterrows():
                st = row.iloc[2]
                url=row.iloc[3]
                usr_nm=row.iloc[4]
                pass_word=row.iloc[5]
                                                
                self.ck = self._tph[self._tph['State'] == st].copy().reset_index(drop=True)          
                
                print(self.ck)

                if self.ck.empty:
                    continue
                elif st=='TX':
                    required_columns = ['NPI','Claim Type','Account No','Client Number','Last Name','First Name','Street','City','State',
                                    'Zip+4','Gender','Patient date of birth','ID Type','EIN/SSN','Qualifier','Code','DOS','placeOfService',
                                    'Proc ID','Proc','Diag Ref','Qty/Units','Unit Price','NPI/API']
                    
                    self.ck.reindex(columns=required_columns, fill_value='')
                    obj_TX = fin_out()
                    obj_TX.final_process(self.ck,url,usr_nm,pass_word)
                elif st=='OH':
                    required_columns = ['']
                    
                    self.ck.reindex(columns=required_columns, fill_value='')
                    obj_OH = fin_out_OH()
                    obj_OH.final_process_OH(self.ck,url,usr_nm,pass_word)
                elif st=='CT':
                    required_columns = ['']
                    
                    self.ck.reindex(columns=required_columns, fill_value='')
                    obj_CT = fin_out_CT()
                    obj_CT.final_process_CT(self.ck,url,usr_nm,pass_word)

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            print(traceback.format_exc()) 

        print('Compted Online Submittion Process...')

class update(login_db):
    def __init__(self):
        super().__init__()

        self.myconn=self._login_db__connection_string

    def update_qry(self):
        try:
            conn = pyodbc.connect(self.myconn)
            cursor = conn.cursor()
            cursor.execute("UPDATE rules.MCDConfiguration SET userName = 'Sathishbilling', password='Password$2024' WHERE state = 'OH'")                    
            conn.commit()
            cursor.close()
            conn.close()
            print('Update Sussesfull...')
        except Exception as e:
            print('Login Database Error')
            return
        
if  __name__ == '__main__':
    obj = start()
    obj.main_process()

    # obj=update()
    # obj.update_qry()
