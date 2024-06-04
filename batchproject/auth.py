from dataclasses import dataclass
import psycopg2
from sqlalchemy import create_engine
import pandas as pd


@dataclass
class InsuranceDB:
    usuario= 'gaguirre'
    pwd= 'gaguirre'
    Host= 'localhost'
    postgres= 'InsuranceDB'
    conn2 = psycopg2.connect(host= Host, user = usuario, password = pwd, dbname=postgres)
    cursor2 = conn2.cursor()
    engine = create_engine(f'postgresql://{usuario}:{pwd}@{Host}/{postgres}')
    
    def check_user_admin(self, id):

        consulta_sql = f"""
            SELECT  role, name
            FROM clients cl
            WHERE cl.id = '{id}'
        """

        role = pd.read_sql(consulta_sql,  InsuranceDB.engine)

        return role.role.iloc[0], role.name.iloc[0]
    
    def get_user_info(self, id):

        consulta_sql = f"""
            SELECT id, amount_insured, email, inception_date, installment_payment, client_id
            FROM policies pl
            WHERE pl.client_id = '{id}'
        """
        user_data = pd.read_sql(consulta_sql, InsuranceDB.engine)
        return  user_data.iloc[0].to_dict()
    
    def get_user_info_by_name(self, name):
        

        consulta_sql = f"""
            SELECT pl.id, pl.amount_insured, pl.email, pl.inception_date, pl.installment_payment, pl.client_id
            FROM policies pl
            JOIN clients cl ON cl.id = pl.client_id
            WHERE cl.name = '{name}'
        """

        user_data = pd.read_sql(consulta_sql, InsuranceDB.engine)
        if not user_data.empty:
            return user_data.to_dict(orient='records')
        return None


    def get_policies_by_name(self, name):
        consulta_sql = f"""
            SELECT pl.id, pl.amount_insured, pl.email, pl.inception_date, pl.installment_payment
            FROM policies pl
            JOIN clients cl ON cl.id = pl.client_id
            WHERE cl.name = '{name}'
        """
        policies_data = pd.read_sql(consulta_sql, InsuranceDB.engine)
        if not policies_data.empty:
            return policies_data.to_dict(orient='records')
        return []


    def get_user_by_policy_id(self, policy_id):
        consulta_sql = f"""
            SELECT cl.id as client_id, cl.name, cl.email
            FROM policies pl
            JOIN clients cl ON cl.id = pl.client_id
            WHERE pl.id = '{policy_id}'
        """
        user_data = pd.read_sql(consulta_sql, InsuranceDB.engine)
        if not user_data.empty:
            return user_data.iloc[0].to_dict()
        return None
