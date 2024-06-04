from batchproject.auth import InsuranceDB
from flask import Flask, request, render_template,  redirect, url_for

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_id = request.form['user_id']
    role, name_user = InsuranceDB().check_user_admin(str(user_id))
    if role:
        if role in ['admin', 'user']:
            return redirect(url_for('query_user_page', name=name_user,  role=role))
        else:
            return redirect(url_for('unknown', name=name_user))
    else:
        return "ID  not found", 404


@app.route('/query_user_page')
def query_user_page():
    name = request.args.get('name')
    role = request.args.get('role')
    return render_template('user_query.html', user_info=None, name=name, role=role)

@app.route('/query_user', methods=['POST'])
def query_user():
    query_id = request.form['query_id']
    user_info = InsuranceDB().get_user_info(str(query_id))
    if user_info:
        return render_template('user_query.html', user_info=user_info)
    else:
        return "User not found", 404


@app.route('/search_user_page')
def search_user_page():
    role = request.args.get('role')

    return render_template('search_by_name.html', user_info=None, role=role)

@app.route('/search_user', methods=['POST'])
def search_user():
    query_name = request.form['query_name']
    user_info = InsuranceDB().get_user_info_by_name(query_name)
    if user_info:
        return render_template('search_by_name.html', user_info=user_info)
    else:
        return "User not found", 404


@app.route('/search_policies_page')
def search_policies_page():
    name = request.args.get('name')
    role = request.args.get('role')
    if role != 'admin':
        return redirect(url_for('index'))
    return render_template('search_policies_by_name.html', policies_info=None, name=name, role = role)

@app.route('/search_policies', methods=['POST'])
def search_policies():
    query_name = request.form['query_name']
    policies_info = InsuranceDB().get_policies_by_name(query_name)
    if policies_info:
        return render_template('search_policies_by_name.html', policies_info=policies_info)
    else:
        return "User not found", 404



@app.route('/search_user_by_policy_page')
def search_user_by_policy_page():
    name = request.args.get('name')
    role = request.args.get('role')
    if role != 'admin':
        return redirect(url_for('index'))
    return render_template('search_user_by_policy.html', user_info=None, name=name, role = role)


@app.route('/search_user_by_policy', methods=['POST'])
def search_user_by_policy():
    policy_id = request.form['policy_id']
    user_info = InsuranceDB().get_user_by_policy_id(policy_id)
    if user_info:
        return render_template('search_user_by_policy.html', user_info=user_info)
    else:
        return "User not found", 404



@app.route('/admin')
def admin():
    name = request.args.get('name')
    return f"<h1>Welcome Admin, {name}</h1>"

@app.route('/user')
def user():
    name = request.args.get('name')
    return f"<h1>Welcome User, {name}</h1>"

@app.route('/unknown')
def unknown():
    name = request.args.get('name')
    return f"<h1>Unknown role {name}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
