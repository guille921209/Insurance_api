from dataclasses import dataclass
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from flask import Flask, request, render_template, send_from_directory, redirect, url_for

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_id = request.form['user_id']
    role, name_user = InsuranceDB().check_user_admin(str(user_id))
    if role:
        if role in ['admin', 'user']:
            return redirect(url_for('query_user_page', name=name_user))
        else:
            return redirect(url_for('unknown', name=name_user))
    else:
        return "ID no encontrado", 404


@app.route('/query_user_page')
def query_user_page():
    name = request.args.get('name')
    return render_template('user_query.html', user_info=None, name=name)

@app.route('/query_user', methods=['POST'])
def query_user():
    query_id = request.form['query_id']
    user_info = InsuranceDB().get_user_info(str(query_id))
    if user_info:
        return render_template('user_query.html', user_info=user_info)
    else:
        return "Usuario no encontrado", 404

@app.route('/search_user_page')
def search_user_page():
    name = request.args.get('name')
    return render_template('search_by_name.html', user_info=None, name=name)

@app.route('/search_user', methods=['POST'])
def search_user():
    query_name = request.form['query_name']
    user_info = InsuranceDB().get_user_info_by_name(query_name)
    return render_template('search_by_name.html', user_info=user_info)
    

@app.route('/search_policies_page')
def search_policies_page():
    name = request.args.get('name')
    return render_template('search_policies_by_name.html', policies_info=None, name=name)

@app.route('/search_policies', methods=['POST'])
def search_policies():
    query_name = request.form['query_name']
    policies_info = InsuranceDB().get_policies_by_name(query_name)
    return render_template('search_policies_by_name.html', policies_info=policies_info)

@app.route('/search_user_by_policy_page')
def search_user_by_policy_page():
    name = request.args.get('name')
    return render_template('search_user_by_policy.html', user_info=None, name=name)


@app.route('/search_user_by_policy', methods=['POST'])
def search_user_by_policy():
    policy_id = request.form['policy_id']
    user_info = InsuranceDB().get_user_by_policy_id(policy_id)
    return render_template('search_user_by_policy.html', user_info=user_info)

@app.route('/admin')
def admin():
    name = request.args.get('name')
    return f"<h1>Bienvenido Administrador, {name}</h1>"

@app.route('/user')
def user():
    name = request.args.get('name')
    return f"<h1>Bienvenido Usuario, {name}</h1>"

@app.route('/unknown')
def unknown():
    name = request.args.get('name')
    return f"<h1>Rol Desconocido para {name}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
    # id = 'a0ece5db-cd14-4f21-812f-966633e7be86'
    # InsuranceDB().check_user_admin(id)