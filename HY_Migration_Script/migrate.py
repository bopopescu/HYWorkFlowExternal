# -*- coding: utf-8 -*-

import pyodbc
import sqlite3
from sqlite3 import Error
from config import config

def create_conn_src(config):

    db_user = config['db_user']
    db_password = config['db_password']
    db_host = config['db_host']
    db_name = config['db_name']

    #driver = "FreeTDS"
    driver = "SQL Server"
    connection_string = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format(driver,db_host,db_name,db_user,db_password)
    conn = pyodbc.connect(connection_string, autocommit=True)
    return conn

def create_conn_dst(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    return conn

def check_tb_map(conn):
    c = conn.cursor()
    sql_create =  """ CREATE TABLE IF NOT EXISTS uuid_map (tb_name VARCHAR(100),uuid_src VARCHAR(200),id_dst integer); """
    sql_index = """ CREATE INDEX IF NOT EXISTS idx_uuid_map ON uuid_map (tb_name, uuid_src, id_dst); """
        
    c.execute("begin")
    try:
        c.execute(sql_create)
        c.execute(sql_index)
        c.execute("commit")
        return True
    except Error as e:
        print("Table creation failed: uuid_map")
        print(e)
        c.execute("rollback")
        print("Rollback performed.")
        return False

def migrate_doctype(conn_src, conn_dst):
    table_name = "administration_documenttypemaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [TransTyp],[TypCde],[TypNme],[AttchPath],[IsActive] FROM [dbo].[OBJT]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            document_type_code = row[1]
            document_type_name = row[2]
            attachment_path = row[3]
            is_active = row[4]
            running_number = 0
            
            params = (document_type_code,document_type_name,attachment_path,running_number,is_active)
            sql = f"INSERT INTO {table_name} (document_type_code,document_type_name,attachment_path,running_number,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_status(conn_src, conn_dst):
    table_name = "administration_statusmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()

    sql = "SELECT [StsID],[StsCde],[StsNme],[DocTypeID],[IsActive] FROM [dbo].[OSTS]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())

    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            status_code = row[1]
            status_name = row[2]
            uuid_document_type_id = row[3]
            is_active = row[4]
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get document_type_id
            ar_param = ("administration_documenttypemaintenance",uuid_document_type_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                document_type_id = 0
                print(f"Unable to find document type id {uuid_document_type_id}")
            else:
                document_type_id = result[0]
            
            params = (status_code,status_name,document_type_id,is_active)
            sql = f"INSERT INTO {table_name} (status_code,status_name,document_type_id,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_transactiontype(conn_src, conn_dst):
    table_name = "administration_transactiontypemaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [TypID],[TypNme],[ObjType],[IsActive] FROM [dbo].[OUTL]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            transaction_type_name = row[1]
            uuid_document_type_id = row[2]
            is_active = row[3]
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get document_type_id
            ar_param = ("administration_documenttypemaintenance",uuid_document_type_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            document_type_id = result[0]
            
            params = (transaction_type_name,document_type_id,is_active)
            sql = f"INSERT INTO {table_name} (transaction_type_name,document_type_id,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_branch(conn_src, conn_dst):

    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ID],[BranchCde],[BranchNme],[IsActive] FROM [dbo].[OBRH]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            params = (row[2],row[3])
            sql = "INSERT INTO administration_branchmaintenance (branch_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = ("administration_branchmaintenance",uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_region(conn_src, conn_dst):

    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [RegionID],[RegionNme],[IsActive] FROM [dbo].[ORGN]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute("delete from administration_regionmaintenance")
    cur_dst.execute("delete from uuid_map where tb_name = 'administration_regionmaintenance'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            params = (row[1],row[2])
            sql = "INSERT INTO administration_regionmaintenance (region_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = ("administration_regionmaintenance",uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_currency(conn_src, conn_dst):

    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [CurrID],[CurrNme],[Rate],[Alphabet],[IsActive] FROM [dbo].[OCUR]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute("delete from administration_currencymaintenance")
    cur_dst.execute("delete from uuid_map where tb_name = 'administration_currencymaintenance'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            currency_name = row[1]
            rate = row[2]
            alphabet = row[3]
            is_active = row[4]
            
            if rate is None:
                rate = 1
            
            params = (currency_name,rate,alphabet,is_active)
            sql = "INSERT INTO administration_currencymaintenance (currency_name,rate,alphabet,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            currency_id = cur_dst.lastrowid
            params = ("administration_currencymaintenance",uuid_src,currency_id)
            cur_dst.execute(sql,params)

            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_dept(conn_src, conn_dst):

    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [DptID],[DptNme],[IsActive] FROM [dbo].[ODPT]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute("delete from administration_departmentmaintenance")
    cur_dst.execute("delete from uuid_map where tb_name = 'administration_departmentmaintenance'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            department_name = row[1]
            is_active = row[2]
            params = (department_name,is_active)
            sql = "INSERT INTO administration_departmentmaintenance (department_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = ("administration_departmentmaintenance",uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")
        
def migrate_country(conn_src, conn_dst):
    table_name = "administration_countrymaintenance"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [CountryID],[CountryNme],[Alpha-2],[Alpha-3],[ISO_3166-2],[IsActive] FROM [dbo].[OCRY]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            country_name = row[1]
            alpha_2 = row[2]
            alpha_3 = row[3]
            iso3166_2 = row[4]
            is_active = row[5]
            
            if alpha_2 is None:
                alpha_2 = "??"
            if alpha_3 is None:
                alpha_3 = "???"

            #Getting currency_id
            sql = "SELECT [CurrID] FROM [dbo].[OCUR] WHERE [CountryID] = ?"
            cur_chk.execute(sql,(uuid_src,))
            rs_chk = cur_chk.fetchone()
            if rs_chk is None:
                currency_id = 0
            else:
                uuid_currency_id = rs_chk[0]
                sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
                ar_param = ("administration_currencymaintenance",uuid_currency_id)
                cur_dst.execute(sql,ar_param)
                result = cur_dst.fetchone()
                currency_id = result[0]
            
            params = (country_name,alpha_2,alpha_3,iso3166_2,currency_id,is_active)
            sql = f"INSERT INTO {table_name} (country_name,alpha_2,alpha_3,iso3166_2,currency_id,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_state(conn_src, conn_dst):
    table_name = "administration_statemaintenance"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [StateID],[CountryCde],[StateNme],[Capital],[IsActive] FROM [dbo].[OSTT]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            CountryCde = row[1]
            state_name = row[2]
            capital = row[3]
            is_active = row[4]
            
            if capital is None:
                capital = "N/A"
            
            #Getting country_id        
            sql = "SELECT [CountryID] FROM [dbo].[OCRY] WHERE [Alpha-2] = ?"
            cur_chk.execute(sql,(CountryCde,))
            rs_ocry = cur_chk.fetchone()
            if rs_ocry is None:
                country_id = 0
                print(f"Unable to find {CountryCde}")
            else:
                uuid_country_id = rs_ocry[0]
                sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
                ar_param = ("administration_countrymaintenance",uuid_country_id)
                cur_dst.execute(sql,ar_param)
                result = cur_dst.fetchone()
                country_id = result[0]
       
                
            params = (state_name,capital,country_id,is_active)
            sql = f"INSERT INTO {table_name} (state_name,capital,country_id,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_comp(conn_src, conn_dst):

    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [CompID],[ShrtName],[CompNme],[BranchID],[BRN],[TaxIdNum1],[TaxIdNum2],[BaseCurrID],[RegionID],[IsActive] FROM [dbo].[COMP]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            short_name = row[1]
            company_name = row[2]
            uuid_branch_id = row[3]
            business_registration_no = row[4]
            tax_id_1 = row[5]
            tax_id_2 = row[6]
            uuid_currency_id = row[7]
            uuid_region_id = row[8]
            is_active = row[9]
            
            if tax_id_1 is None:
                tax_id_1 = "N/A"
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            #Get branch_id.
            ar_param = ("administration_branchmaintenance",uuid_branch_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            branch_id = result[0]
            
            #Get currency_id
            ar_param = ("administration_currencymaintenance",uuid_currency_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                currency_id = 0
                print(f"Unable to find currency {uuid_currency_id}")
            else:
                currency_id = result[0]
            
            #Get region_id
            ar_param = ("administration_regionmaintenance",uuid_region_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                region_id = 0
                print(f"Unable to find currency {uuid_region_id}")
            else:
                region_id = result[0]
            
            params = (short_name,company_name,branch_id,business_registration_no,tax_id_1,tax_id_2,currency_id,region_id,is_active)
            sql = "INSERT INTO administration_companymaintenance (short_name,company_name,branch_id,business_registration_no,tax_id_1,tax_id_2,currency_id,region_id,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,?,?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = ("administration_companymaintenance",uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_compcontact(conn_src, conn_dst):

    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [CompID],[DftlSAddID] FROM [dbo].[COMP]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    try:
        rec_count = 0
        for row in recordset:
            uuid_comp_id = row[0]
            uuid_add_id = row[1] # Not defined in new db
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
                
            #Get company_id.
            ar_param = ("administration_companymaintenance",uuid_comp_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            company_id = result[0]
            
            sql = "SELECT [AddrID],[AddrNme],[AddLine1],[AddLine2],[AddLine3],[AddLine4],[Zip],[State],[Country] FROM [dbo].[OADR] WHERE [CompID] = ?"
            cur_chk.execute(sql,(uuid_comp_id,))
            rs_add = list(cur_chk.fetchall())
            for rw_add in rs_add:
                uuid_src = rw_add[0]
                address_name = rw_add[1]
                address1 = rw_add[2]
                address2 = rw_add[3]
                address3 = rw_add[4]
                address4 = rw_add[5]
                address_zip = rw_add[6]
                uuid_state_id = rw_add[7]
                uuid_country_id = rw_add[8]
                
                sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
                
                #Get country_id.
                ar_param = ("administration_countrymaintenance",uuid_country_id)
                cur_dst.execute(sql,ar_param)
                result = cur_dst.fetchone()
                if result is None:
                    country_id = 0
                    print(f"Unable to find country {uuid_country_id}")
                else:
                    country_id = result[0]
                
                #Get state_id.
                ar_param = ("administration_statemaintenance",uuid_state_id)
                cur_dst.execute(sql,ar_param)
                result = cur_dst.fetchone()
                if result is None:
                    state_id = 0
                    print(f"Unable to find state {uuid_state_id}")
                else:
                    state_id = result[0]
            
                params = (address_name,address1,address2,address3,address4,address_zip,company_id,country_id,state_id)
                sql = "INSERT INTO administration_companyaddressdetail (address_name,address1,address2,address3,address4,address_zip,company_id,country_id,state_id) VALUES(?,?,?,?,?,?,?,?,?)"
                cur_dst.execute(sql,params)
                sql = "INSERT INTO uuid_map VALUES (?,?,?)"
                params = ("administration_companyaddressdetail",uuid_src,cur_dst.lastrowid)
                cur_dst.execute(sql,params)
                cur_dst.execute("commit")
                rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")


def migrate_emp_group(conn_src, conn_dst):
    table_name = "administration_employeegroupmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [GroupID],[GroupNme],[IsActive] FROM [dbo].[USRG]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            group_name = row[1]
            is_active = row[2]
            params = (group_name,is_active)
            sql = f"INSERT INTO {table_name} (group_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_emp_position(conn_src, conn_dst):
    table_name = "administration_employeepositionmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT DISTINCT[Position] FROM [dbo].[OEMP]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    
    try:
        rec_count = 0
        for row in recordset:
            
            position_name = row[0]
            is_active = 1
            
            params = (position_name,is_active)
            sql = f"INSERT INTO {table_name} (position_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_user(conn_src, conn_dst):
    table_name = "administration_usermaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [UsrID],[UsrCde],[UsrNme],[GroupCde],[CompID],[SignaturePic] FROM [dbo].[OUSR]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            user_code = row[1] 
            user_name = row[2]
            user_group = row[3]
            uuid_company_id = row[4]
            signature = row[5]
            
            if signature is None:
                signature = "N/A"
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get company_id
            ar_param = ("administration_companymaintenance",uuid_company_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            company_id = result[0]
            
            params = (user_code,user_name,user_group,company_id,signature)
            sql = f"INSERT INTO {table_name} (user_code,user_name,user_group,company_id,signature) VALUES(?,?,?,?,?)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_auth_group(conn_src, conn_dst):
    table_name = "auth_group"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [GroupID],[GroupNme],[IsActive] FROM [dbo].[USRG]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            group_name = row[1]
            
            params = (group_name,)
            sql = f"INSERT INTO {table_name} (name) VALUES(?)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_auth_user(conn_src, conn_dst):
    table_name = "auth_user"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [UsrID],[Password],[LastLogin],[UsrNme],[FullNme],[IsActive],[CreationTS],[Group] FROM [dbo].[OUSR]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            password = row[1] 
            last_login = row[2]
            is_superuser = 1
            username = row[3]
            first_name = row[4]
            email = ""
            is_staff = 1
            is_active = row[5]
            date_joined = row[6]
            last_name = ""
            
            uuid_group = row[7]
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            #Get auth_group_id
            ar_param = ("auth_group",uuid_group)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            auth_group_id = result[0]
            
            #User
            params = (password,last_login,is_superuser,username,first_name,email,is_staff,is_active,date_joined,last_name)
            sql = f"INSERT INTO {table_name} (password,last_login,is_superuser,username,first_name,email,is_staff,is_active,date_joined,last_name) VALUES(?,?,?,?,?,?,?,?,?,?)"
            cur_dst.execute(sql,params)
            auth_user_id = cur_dst.lastrowid
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,auth_user_id)
            cur_dst.execute(sql,params)
            
            #User-Group
            params = (auth_user_id,auth_group_id)
            sql = f"INSERT INTO auth_user_groups (user_id,group_id) VALUES(?,?)"
            cur_dst.execute(sql,params)
            
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_employee(conn_src, conn_dst):
    table_name = "administration_employeemaintenance"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [EmpID],[EmpNme],[Gender],[DOB],[Position],[IsActive],[Email],[UsrID],[ID_Parent] FROM [dbo].[OEMP]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            employee_name = row[1]
            nick_name = ""
            gender = row[2]
            dob = row[3]
            Position = row[4]
            is_active = row[5]
            email = row[6]
            uuid_user_id = row[7]
            reporting_officer_id_id = row[8]
            
            
            #Get position_id_id
            sql = "SELECT id FROM administration_employeepositionmaintenance WHERE position_name = ?"
            ar_param = (Position,)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            position_id_id = result[0]
            
            #Get auth_user_id
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            ar_param = ("auth_user",uuid_user_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            auth_user_id = result[0]
            
            #Get employee_group_id
            sql = "SELECT id FROM administration_employeegroupmaintenance WHERE group_name = (SELECT name from auth_group WHERE id = (SELECT group_id FROM auth_user_groups WHERE user_id = ?))"
            ar_param = (auth_user_id,)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            employee_group_id = result[0]
            
            #Getting employee_signature
            sql = "SELECT [SignaturePic] FROM [dbo].[OUSR] WHERE [UsrID] = ?"
            cur_chk.execute(sql,(uuid_user_id,))
            rs_chk = cur_chk.fetchone()
            if rs_chk is None:
                print(f"Unable to find signature for {uuid_user_id}")
                employee_signature = "N/A"
            else:
                if rs_chk[0] is None:
                    employee_signature = "N/A"
                else:
                    employee_signature = rs_chk[0]
                
            #User
            params = (employee_name,nick_name,gender,dob,position_id_id,is_active,employee_group_id,employee_signature,email,auth_user_id,reporting_officer_id_id)
            sql = f"INSERT INTO {table_name} (employee_name,nick_name,gender,dob,position_id_id,is_active,employee_group_id,employee_signature,email,user_id,reporting_officer_id_id,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,?,?,?,?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            auth_user_id = cur_dst.lastrowid
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,auth_user_id)
            cur_dst.execute(sql,params)
            
            
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_employeedept(conn_src, conn_dst):
    table_name = "administration_employeedepartmentmaintenance"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [EmpID],[DptID] FROM [dbo].[OEMP]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    
    try:
        rec_count = 0
        for row in recordset:
            uuid_emp_id = row[0]
            uuid_dept_id = row[1]
                        
            #Get employee_id
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            ar_param = ("administration_employeemaintenance",uuid_emp_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                employee_id = 0
                print(f"Unable to find employee {uuid_emp_id}")
            else:
                employee_id = result[0]
            
            #Get department_id
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            ar_param = ("administration_departmentmaintenance",uuid_dept_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                department_id = 0
                print(f"Unable to find department {uuid_dept_id}")
            else:
                department_id = result[0]
            
            if employee_id != 0 and department_id != 0:
                params = (employee_id,department_id)
                sql = f"INSERT INTO {table_name} (employee_id,department_id,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
                cur_dst.execute(sql,params)
                cur_dst.execute("commit")
                rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_employeecomp(conn_src, conn_dst):
    table_name = "administration_employeecompanymaintenance"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT E.[EmpID],C.[CompID] FROM [dbo].[OEMP] E JOIN [dbo].[OUSR] C ON (E.UsrID=C.UsrID)"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    
    try:
        rec_count = 0
        for row in recordset:
            uuid_emp_id = row[0]
            uuid_comp_id = row[1]
                        
            #Get employee_id
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            ar_param = ("administration_employeemaintenance",uuid_emp_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                employee_id = 0
                print(f"Unable to find employee {uuid_emp_id}")
            else:
                employee_id = result[0]
            
            #Get company_id
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            ar_param = ("administration_companymaintenance",uuid_comp_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                company_id = 0
                print(f"Unable to find company {uuid_comp_id}")
            else:
                company_id = result[0]
            
            if employee_id != 0 and company_id != 0:
                params = (employee_id,company_id)
                sql = f"INSERT INTO {table_name} (employee_id,company_id) VALUES(?,?)"
                cur_dst.execute(sql,params)
                cur_dst.execute("commit")
                rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_vendorcat(conn_src, conn_dst):
    table_name = "administration_vendorcategorymaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ID],[VendorCatDesc],[IsActive] FROM [dbo].[OVCT]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            vendor_category_name = row[1]
            is_active = row[2]
            params = (vendor_category_name,is_active)
            sql = f"INSERT INTO {table_name} (vendor_category_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_vendorgrp(conn_src, conn_dst):
    table_name = "administration_vendorgroupmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [GrpID],[GrpName],[IsActive] FROM [dbo].[BPMG]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            group_name = row[1]
            is_active = row[2]
            params = (group_name,is_active)
            sql = f"INSERT INTO {table_name} (group_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_vendor(conn_src, conn_dst):
    table_name = "administration_vendormasterdata"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ID],[BPNme],[BRN],[TaxIdNum],[TaxIdNum2],[RegType],[CurrID],[Group],[VendorCat],[IsPQ],[IsActive] FROM [dbo].[BPM0] WHERE BPTypCde = 'S'"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            vendor_name = row[1]
            business_registration_no = row[2]
            tax_id_1 = row[3]
            tax_id_2 = row[4]
            RegType = row[5]
            if RegType == "Company":
                is_company = 1
            else:
                is_company = 0
            uuid_currency_id = row[6]
            uuid_vendor_group_id = row[7]
            VendorCat = row[8]
            is_qualified = row[9]
            is_active = row[10]
            
            if tax_id_1 is None:
                tax_id_1 = "N/A"
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get currency_id
            ar_param = ("administration_currencymaintenance",uuid_currency_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            currency_id = result[0]
            
            #Get vendor_group_id
            ar_param = ("administration_vendorgroupmaintenance",uuid_vendor_group_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            vendor_group_id = result[0]
            
            #Getting vendor_category_id
            sql = "SELECT [ID] FROM [dbo].[OVCT] WHERE [VendorCat] LIKE ?"
            cur_chk.execute(sql,(VendorCat + "%",))
            rs_chk = cur_chk.fetchone()
            if rs_chk is None:
                print(f"Unable to find {VendorCat}")
                vendor_category_id = 0
            else:
                uuid_vendor_cat_id = rs_chk[0]
                sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
                ar_param = ("administration_vendorcategorymaintenance",uuid_vendor_cat_id)
                cur_dst.execute(sql,ar_param)
                result = cur_dst.fetchone()
                vendor_category_id = result[0]
            
            params = (vendor_name,business_registration_no,tax_id_1,tax_id_2,is_company,currency_id,vendor_group_id,vendor_category_id,is_qualified,is_active)
            sql = f"INSERT INTO {table_name} (vendor_name,business_registration_no,tax_id_1,tax_id_2,is_company,currency_id,vendor_group_id,vendor_category_id,is_qualified,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,?,?,?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_vendor_address(conn_src, conn_dst):
    table_name = "administration_vendoraddressdetail"
    cur_src = conn_dst.cursor()
    cur_chk = conn_dst.cursor()
    cur_dst = conn_dst.cursor()
    cur_dat = conn_src.cursor()
    
    sql = "SELECT uuid_src,id_dst FROM uuid_map WHERE tb_name = 'administration_vendormasterdata'"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_vendor = row[0]
            vendor_id = row[1]
            
            #print(f"Vendor {uuid_vendor}")
            
            #Getting vendor address
            sql = "SELECT [AddrID],[AddrNme],[AddLine1],[AddLine2],[AddLine3],[AddLine4],[Zip],[State],[Country] FROM [dbo].[OADR] WHERE [BPId] = ?"
            cur_dat.execute(sql,(uuid_vendor,))
            rs_dat = list(cur_dat.fetchall())
            for rw_dat in rs_dat:
                uuid_src = rw_dat[0]
                address_name = rw_dat[1]
                address1 = rw_dat[2]
                address2 = rw_dat[3]
                address3 = rw_dat[4]
                address4 = rw_dat[5]
                address_zip = str(rw_dat[6])
                uuid_state_id = rw_dat[7]
                uuid_country_id = rw_dat[8]

                #Fetching state_id
                sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
                ar_param = ("administration_statemaintenance",uuid_state_id)
                cur_chk.execute(sql,ar_param)
                result = cur_chk.fetchone()
                if result is None:
                    print(f"Unable to find state {uuid_state_id}")
                    state_id = 0
                else:
                    state_id = result[0]
                
                #Fetching country_id
                sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
                ar_param = ("administration_countrymaintenance",uuid_country_id)
                cur_chk.execute(sql,ar_param)
                result = cur_chk.fetchone()
                if result is None:
                    print(f"Unable to find country {uuid_country_id}")
                    country_id = 0
                else:
                    country_id = result[0]
                
                params = (address_name,address1,address2,address3,address4,address_zip,state_id,country_id,vendor_id)
                sql = f"INSERT INTO {table_name} (address_name,address1,address2,address3,address4,address_zip,state_id,country_id,vendor_id) VALUES(?,?,?,?,?,?,?,?,?)"
                cur_dst.execute(sql,params)
                sql = "INSERT INTO uuid_map VALUES (?,?,?)"
                params = (table_name,uuid_src,cur_dst.lastrowid)
                cur_dst.execute(sql,params)
                cur_dst.execute("commit")
                rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")
        
def migrate_memotemplate(conn_src, conn_dst):
    table_name = "administration_memotemplatemaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ID],[MemoDesc],[URL],[IsActive] FROM [dbo].[MEMT]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            memo_template_name = row[1]
            template_htmldesign = row[2]
            is_active = row[3]
            params = (memo_template_name,template_htmldesign,is_active)
            sql = f"INSERT INTO {table_name} (memo_template_name,template_htmldesign,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_location(conn_src, conn_dst):
    table_name = "administration_locationmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ID],[LocNme],[IsActive] FROM [dbo].[OLCT]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            loc_name = row[1]
            is_active = row[2]
            params = (loc_name,is_active)
            sql = f"INSERT INTO {table_name} (loc_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
            
        print(f"{rec_count} records migrated.")
        
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_tax(conn_src, conn_dst):
    table_name = "administration_taxmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ID],[TaxCde],[TaxNme],[IsActive] FROM [dbo].[OTXC]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            tax_code = row[1]
            tax_name = row[2]
            is_active = row[3]
            
            rate = 0
            
            params = (tax_code,tax_name,rate,is_active)
            sql = f"INSERT INTO {table_name} (tax_code,tax_name,rate,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
            
        print(f"{rec_count} records migrated.")
        
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_project(conn_src, conn_dst):
    table_name = "administration_projectmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ProjID],[ProjCde],[ProjNme],[PhasNme],[SubPhasName],[EffFrom],[EffTo],[CompID] FROM [dbo].[OPRJ]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            project_code = row[1]
            project_name = row[2]
            phase_name = row[3]
            sub_phase_name = row[4]
            effect_start_date = row[5]
            effect_end_date = row[6]
            uuid_company_id = row[7]
            
            if phase_name is None:
                phase_name = "N/A"
            if sub_phase_name is None:
                sub_phase_name = "N/A"
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get company_id
            ar_param = ("administration_companymaintenance",uuid_company_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            company_id = result[0]
            
            params = (project_code,project_name,phase_name,sub_phase_name,effect_start_date,effect_end_date,company_id)
            sql = f"INSERT INTO {table_name} (project_code,project_name,phase_name,sub_phase_name,effect_start_date,effect_end_date,company_id,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_memo(conn_src, conn_dst):
    table_name = "memo_memo"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [DocKey],[DocNum],[StsID],[PostingDate],[Subject],[CompID],[DpmtID],[ProjID],[Remarks],[Rev] FROM [dbo].[MEM0]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            document_number = row[1]
            status_id = row[2]
            submit_date = row[3]
            subject = row[4]
            uuid_company_id = row[5]
            uuid_department_id = row[6]
            uuid_project_id = row[7]
            details = row[8]
            #uuid_template_id = row[9]
            template_id = 0
            revision = row[9]
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get company_id
            ar_param = ("administration_companymaintenance",uuid_company_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            company_id = result[0]
            
            #Get department_id
            ar_param = ("administration_departmentmaintenance",uuid_department_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            department_id = result[0]
            
            #Get project_id
            ar_param = ("administration_projectmaintenance",uuid_project_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            project_id = result[0]
            
            #Get template_id
            """
            ar_param = ("administration_memotemplatemaintenance",uuid_template_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            template_id = result[0]
            """

            params = (document_number,status_id,submit_date,subject,company_id,department_id,project_id,details,template_id,revision)
            sql = f"INSERT INTO {table_name} (document_number,status_id,submit_date,subject,company_id,department_id,project_id,details,template_id,revision) VALUES(?,?,?,?,?,?,?,?,?,?)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_paymentterm(conn_src, conn_dst):
    table_name = "administration_paymenttermmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [TermID],[TermDsc],[Days],[IsActive] FROM [dbo].[OPYT]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            description = row[1]
            days = row[2]
            is_active = row[3]
            params = (description,days,is_active)
            sql = f"INSERT INTO {table_name} (description,days,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1

        print(f"{rec_count} records migrated.")
        
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_paymentmode(conn_src, conn_dst):
    table_name = "administration_paymentmodemaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [PayID],[PayNme],[IsActive] FROM [dbo].[OPYM]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            payment_mode_name = row[1]
            is_active = row[2]
            params = (payment_mode_name,is_active)
            sql = f"INSERT INTO {table_name} (payment_mode_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
            
        print(f"{rec_count} records migrated.")
        
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")
       
def migrate_paymentrequest(conn_src, conn_dst):
    table_name = "payment_paymentrequest"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [DocKey],[Rev],[DocNum],[StsID],[PostDate],[Subject],[Reference],[CompID],[CurrID],[ProjID],[BPID],[DiscAmtLC],[DiscPrcnt],[PayMode],[Remark],[SubTotLC],[TaxAmtLC],[TotalLC],[TransType] FROM [dbo].[OPYR]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            revision = row[1]
            document_number = row[2]
            uuid_status_id = row[3]
            submit_date = row[4]
            subject = row[5]
            reference = row[6]
            uuid_company_id = row[7]
            uuid_currency_id = row[8]
            uuid_project_id = row[9]
            uuid_vendor_id = row[10]
            discount_amount = str(row[11])
            discount_rate = str(row[12])
            #uuid_payment_mode_id = row[13]
            PayMode = row[13]
            remarks = row[14]
            sub_total = str(row[15])
            tax_amount = str(row[16])
            total_amount = str(row[17])
            uuid_transaction_type_id = row[18]
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get status_id
            ar_param = ("administration_statusmaintenance",uuid_status_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            status_id = result[0]
            
            #Get company_id
            ar_param = ("administration_companymaintenance",uuid_company_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            company_id = result[0]
            
            #Get currency_id
            ar_param = ("administration_currencymaintenance",uuid_currency_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            currency_id = result[0]
            
            #Get project_id
            ar_param = ("administration_projectmaintenance",uuid_project_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            project_id = result[0]
            
            #Get vendor_id
            ar_param = ("administration_vendormasterdata",uuid_vendor_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                vendor_id = 0
                print(f"Unable to find vendor {uuid_vendor_id}")
            else:
                vendor_id = result[0]
            
            #Getting payment_mode_id
            sql = "SELECT [PayID] FROM [dbo].[OPYM] WHERE [PayNme] LIKE ?"
            cur_chk.execute(sql,(PayMode + "%",))
            rs_chk = cur_chk.fetchone()
            if rs_chk is None:
                payment_mode_id = 0
                print(f"Unable to find payment mode in source {PayMode}")
            else:
                uuid_payment_mode_id = rs_chk[0]
                sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
                ar_param = ("administration_paymentmodemaintenance",uuid_payment_mode_id)
                cur_dst.execute(sql,ar_param)
                result = cur_dst.fetchone()
                if result is None:
                    payment_mode_id = 0
                    print(f"Unable to find payment mode in map {uuid_payment_mode_id}")
                else:
                    payment_mode_id = result[0]
            
            #Get transaction_type_id
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            ar_param = ("administration_transactiontypemaintenance",uuid_transaction_type_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            try:
                transaction_type_id = result[0]
            except:
                transaction_type_id = "NULL"   

            params = (revision,document_number,status_id,submit_date,subject,reference,company_id,currency_id,project_id,vendor_id,discount_amount,discount_rate,payment_mode_id,remarks,sub_total,tax_amount,total_amount,transaction_type_id)
            sql = f"INSERT INTO {table_name} (revision,document_number,status_id,submit_date,subject,reference,company_id,currency_id,project_id,vendor_id,discount_amount,discount_rate,payment_mode_id,remarks,sub_total,tax_amount,total_amount,transaction_type_id,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(params)
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_paymentrequestdtl(conn_src, conn_dst):
    table_name = "payment_paymentrequestdetail"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [DocKey],[LineNum],[ItemDesc],[Price],[LineTotalLC],[TaxID],[TaxAmtLC] FROM [dbo].[PYR2]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_py_id = row[0]
            linenum = row[1]
            item_description = row[2]
            price = str(row[3])
            line_total = str(row[4])
            uuid_tax_id = row[5]
            line_taxamount = str(row[6])
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get py_id
            ar_param = ("payment_paymentrequest",uuid_py_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                py_id = 0
                print(f"Unable to find payment payment request {uuid_py_id}")
            else:
                py_id = result[0]
            
            #Get tax_id
            ar_param = ("administration_taxmaintenance",uuid_tax_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                tax_id = 'NULL'
            else:
                tax_id = result[0]
            
            if py_id != 0:
                params = (py_id,linenum,item_description,price,line_total,tax_id,line_taxamount)
                sql = f"INSERT INTO {table_name} (py_id,linenum,item_description,price,line_total,tax_id,line_taxamount) VALUES(?,?,?,?,?,?,?)"
                cur_dst.execute(sql,params)
                
                cur_dst.execute("commit")
                rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(params)
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_itemgroup(conn_src, conn_dst):
    table_name = "administration_itemgroupsmaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ID],[ItmsGrpNme],[IsActive] FROM [dbo].[ITMG]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            item_group_name = row[1]
            is_active = row[2]
            
            params = (item_group_name,is_active)
            sql = f"INSERT INTO {table_name} (item_group_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
            
        print(f"{rec_count} records migrated.")
        
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_itemcategory(conn_src, conn_dst):
    table_name = "Inventory_itemcategorymaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [SubCID],[SubCatDesc],[IsActive] FROM [dbo].[SCAT]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            category_name = row[1]
            is_active = row[2]
            params = (category_name,is_active)
            sql = f"INSERT INTO {table_name} (category_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
            
        print(f"{rec_count} records migrated.")
        
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_uom(conn_src, conn_dst):
    table_name = "administration_uommaintenance"
    cur_src = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ID],[UomName],[IsActive] FROM [dbo].[UOM0]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            uom_name = row[1]
            is_active = row[2]
            params = (uom_name,is_active)
            sql = f"INSERT INTO {table_name} (uom_name,is_active,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
            
        print(f"{rec_count} records migrated.")
        
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")


def migrate_item(conn_src, conn_dst):
    table_name = "Inventory_item"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [ItemID],[ItemCode],[ItemDesc],[Origin],[Spec],[HSCode],[MinQty],[MinOrdQty],[SpqQty],[LeadTime],[Comments],[IsActive],[ItemGrpID],[UomID],[SubCatID],[ItemType] FROM [dbo].[ITM0]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            item_code = row[1]
            item_description = row[2]
            origin = row[3]
            specification = row[4]
            hs_code = row[5]
            minimum_quantity = str(row[6])
            minimum_order_quantity = str(row[7])
            standard_packing_quantity = str(row[8])
            leadtime = row[9]
            remarks = row[10]
            is_active = row[11]
            item_class_id = 0
            uuid_item_group_id = row[12]
            uuid_item_uom_id = row[13]
            uuid_item_category_id = row[14]
            item_subcategory_id = 0
            item_subsubcategory_id = 0
            item_type = row[15]
            
            if origin is None or origin == "":
                origin = "N/A"
            if hs_code is None or hs_code == "":
                hs_code = "N/A"
            if remarks is None or remarks == "":
                remarks = "N/A"
            if specification is None or specification == "":
                specification = "N/A"
            if leadtime is None:
                leadtime = "0"
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get item_group_id
            ar_param = ("administration_itemgroupsmaintenance",uuid_item_group_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                item_group_id = 0
                print(f"Unable to find item group id {uuid_item_group_id}")
            else:
                item_group_id = result[0]
            
            #Get uom_id
            ar_param = ("administration_uommaintenance",uuid_item_uom_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            item_uom_id = result[0]
            
            #Get item_category_id
            ar_param = ("Inventory_itemcategorymaintenance",uuid_item_category_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                item_category_id = 0
                print(f"Unable to find item group id {uuid_item_category_id}")
            else:
                item_category_id = result[0]
            
            params = (item_code,item_description,origin,specification,hs_code,minimum_quantity,minimum_order_quantity,standard_packing_quantity,leadtime,remarks,is_active,item_class_id,item_group_id,item_uom_id,item_category_id,item_subcategory_id,item_subsubcategory_id,item_type)
            sql = f"INSERT INTO {table_name} (item_code,item_description,origin,specification,hs_code,minimum_quantity,minimum_order_quantity,standard_packing_quantity,leadtime,remarks,is_active,item_class_id,item_group_id,item_uom_id,item_category_id,item_subcategory_id,item_subsubcategory_id,item_type,created_by_id,created_timestamp,modified_by_id,modified_timestamp) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1,CURRENT_TIMESTAMP,1,CURRENT_TIMESTAMP)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(params)
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")

def migrate_po(conn_src, conn_dst):
    table_name = "purchasing_purchaseorder"
    cur_src = conn_src.cursor()
    cur_chk = conn_src.cursor()
    cur_dst = conn_dst.cursor()
    sql = "SELECT [DocKey],[Rev],[DocNum],[StsID],[PostingDate],[Subject],[BPRefNo],[CompID],[ProjID],[BPID],[DiscPrcnt],[PaySchedule],[TermCde],[Comments],[SubTotLC],[TaxAmtLC],[TotalLC],[CreatedBy],[TransType],[ShipAddr],[DeliveryInstruction],[ShipTo],[CurrID],[FVendID],[FTotalAmt],[SVendID],[STotalAmt],[DiscAmtLC] FROM [dbo].[TPOR]"
    cur_src.execute(sql)
    recordset = list(cur_src.fetchall())
    cur_dst.execute("begin")
    cur_dst.execute(f"delete from {table_name}")
    cur_dst.execute(f"delete from uuid_map where tb_name = '{table_name}'")
    try:
        rec_count = 0
        for row in recordset:
            uuid_src = row[0]
            revision = row[1]
            document_number = row[2]
            uuid_status_id = row[3]
            submit_date = row[4]
            subject = row[5]
            reference = row[6]
            company_id = row[7]
            project_id = row[8]
            uuid_vendor_id = row[9]
            discount = str(row[10])
            payment_schedule = row[11]
            payment_term = row[12]
            remarks = row[13]
            sub_total = str(row[14])
            tax_amount = str(row[15])
            total_amount = str(row[16])
            approval_id = "NULL"
            submit_by_id = row[17]
            uuid_transaction_type_id = row[18]
            billing_address = "NULL"
            delivery_address = row[19]
            delivery_instruction = row[20]
            billing_receiver_id = "NULL"
            uuid_delivery_receiver_id = row[21]
            uuid_currency_id = row[22]
            uuid_comparison_vendor_2_id = row[23]
            
            comparison_vendor_2_amount = str(row[24])
            uuid_comparison_vendor_3_id = row[25]
            comparison_vendor_3_amount = str(row[26])
            vendor_address = "NULL"
            discount_amount = str(row[27])
            
            
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            
            #Get status_id
            ar_param = ("administration_statusmaintenance",uuid_status_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                status_id = "NULL"
                print(f"Unable to find status_id {uuid_status_id}")
            else:
                status_id = result[0]
            
            #Get transaction_type_id
            sql = "SELECT id_dst FROM uuid_map WHERE tb_name = ? and uuid_src = ?"
            ar_param = ("administration_transactiontypemaintenance",uuid_transaction_type_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                transaction_type_id = "NULL"
                print(f"Unable to find status_id {uuid_status_id}")
            else:
                transaction_type_id = result[0]   
            
            #Get delivery_receiver_id
            
            #Get currency_id
            currency_id = 218

            #Get vendor_id
            ar_param = ("administration_vendormasterdata",uuid_vendor_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                vendor_id = "NULL"
                print(f"Unable to find vendor {vendor_id}")
            else:
                vendor_id = result[0]
            
            #Get comparison_vendor_2_id
            ar_param = ("administration_vendormasterdata",uuid_comparison_vendor_2_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                comparison_vendor_2_id = "NULL"
                print(f"Unable to find vendor {uuid_comparison_vendor_2_id}")
            else:
                comparison_vendor_2_id = result[0]

            #Get comparison_vendor_3_id
            ar_param = ("administration_vendormasterdata",uuid_comparison_vendor_3_id)
            cur_dst.execute(sql,ar_param)
            result = cur_dst.fetchone()
            if result is None:
                comparison_vendor_3_id = "NULL"
                print(f"Unable to find vendor {uuid_comparison_vendor_3_id}")
            else:
                comparison_vendor_3_id = result[0]

            # Require modification
            params = (revision,document_number,status_id,submit_date,subject,reference,company_id,currency_id,project_id,vendor_id,discount_amount,discount,remarks,sub_total,tax_amount,total_amount,transaction_type_id,comparison_vendor_2_id,comparison_vendor_2_amount, comparison_vendor_3_id, comparison_vendor_3_amount)
            sql = f"INSERT INTO {table_name} (revision,document_number,status_id,submit_date,subject,reference,company_id,currency_id,project_id,vendor_id,discount_amount,discount,remarks,sub_total,tax_amount,total_amount,transaction_type_id, comparison_vendor_2_id, comparison_vendor_2_amount, comparison_vendor_3_id, comparison_vendor_3_amount) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cur_dst.execute(sql,params)
            sql = "INSERT INTO uuid_map VALUES (?,?,?)"
            params = (table_name,uuid_src,cur_dst.lastrowid)
            cur_dst.execute(sql,params)
            cur_dst.execute("commit")
            rec_count += 1
        print(f"{rec_count} records migrated.")
    except Error as e:
        print(f"Error in SQL statement.  {e}")
        print(params)
        print(f"Last SQL query : {sql}")
        cur_dst.execute("rollback")
        print("Rollback performed.")
        
if __name__ == '__main__':
    #START
    
    #Old DB
    conn_src = create_conn_src(config)
    
    #New DB
    db_path_new = config['db_path_new']
    conn_dst = create_conn_dst(db_path_new)
    #conn_dst.isolation_level = None
    
    if conn_src is not None and conn_dst is not None:
    
        #Preparation
        if check_tb_map(conn_dst) == True:
    
            #Start Migrating
            """
            print("Migrating : Branch")
            migrate_branch(conn_src,conn_dst)
            
            print("Migrating : Department")
            migrate_dept(conn_src,conn_dst)
            
            print("Migrating : Currency")
            migrate_currency(conn_src,conn_dst)
            
            print("Migrating : Country")
            migrate_country(conn_src,conn_dst)
            
            print("Migrating : State")
            migrate_state(conn_src,conn_dst)
            
            print("Migrating : Region")
            migrate_region(conn_src,conn_dst)
            
            print("Migrating : Company")
            migrate_comp(conn_src,conn_dst)
            
            print("Migrating : Location")
            migrate_location(conn_src,conn_dst)
            
            print("Migrating : Document Type")
            migrate_doctype(conn_src,conn_dst)
            
            print("Migrating : Status")
            migrate_status(conn_src,conn_dst)
            
            print("Migrating : Transaction Type")
            migrate_transactiontype(conn_src,conn_dst)
            
            #print("Migrating : User")
            #migrate_user(conn_src,conn_dst)
            
            print("Migrating : User Group")
            migrate_auth_group(conn_src,conn_dst)
            
            print("Migrating : User")
            migrate_auth_user(conn_src,conn_dst)
            
            print("Migrating : Employee Group")
            migrate_emp_group(conn_src,conn_dst)
            
            print("Migrating : Employee Position")
            migrate_emp_position(conn_src,conn_dst)
                                    
            print("Migrating : Vendor Category")
            migrate_vendorcat(conn_src,conn_dst)
            
            print("Migrating : Vendor Group")
            migrate_vendorgrp(conn_src,conn_dst)
            
            print("Migrating : Vendor")
            migrate_vendor(conn_src,conn_dst)
                        
            print("Migrating : Tax")
            migrate_tax(conn_src,conn_dst)
            
            print("Migrating : Memo Template")
            migrate_memotemplate(conn_src,conn_dst)
            
            print("Migrating : Project")
            migrate_project(conn_src,conn_dst)
            
            print("Migrating : Memo")
            migrate_memo(conn_src,conn_dst)
            
            print("Migrating : Payment Term")
            migrate_paymentterm(conn_src,conn_dst)
            
            print("Migrating : Payment Mode")
            migrate_paymentmode(conn_src,conn_dst)
            
            print("Migrating : Payment Request")
            migrate_paymentrequest(conn_src,conn_dst)
            
            print("Migrating : Company Contact Details")
            migrate_compcontact(conn_src,conn_dst)
            
            print("Migrating : Item Group")
            migrate_itemgroup(conn_src,conn_dst)
            
            print("Migrating : Item Category")
            migrate_itemcategory(conn_src,conn_dst)
            
            print("Migrating : UOM")
            migrate_uom(conn_src,conn_dst)
            
            print("Migrating : Item")
            migrate_item(conn_src,conn_dst)
            
            print("Migrating : Employee")
            migrate_employee(conn_src,conn_dst)
                        
            print("Migrating : Vendor Addresses")
            migrate_vendor_address(conn_src,conn_dst)
                        
            print("Migrating : Payment Request Detail")
            migrate_paymentrequestdtl(conn_src,conn_dst)
            
            print("Migrating : Employee Department")
            migrate_employeedept(conn_src,conn_dst)
            
            print("Migrating : Employee Company")
            migrate_employeecomp(conn_src,conn_dst)
            
            print("Migrating : Payment Request Detail")
            migrate_paymentrequestdtl(conn_src,conn_dst)
            """
            print("Migrating : Purchase Order")
            migrate_po(conn_src,conn_dst)
            
            #print("Migrating : Purchase Order Detail")
            #migrate_po_dtl(conn_src, conn_dst)
            
            #End Migrating
            conn_dst.close()
            conn_src.close()
    else:
        if conn_src is None:
            print("Unable to establish source database connection.")
        if conn_dst is None:
            print("Unable to establish destination database connection.")

