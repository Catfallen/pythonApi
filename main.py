from flask import flash,Flask, render_template, request, redirect, url_for,jsonify
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(
        database='python',
        host='localhost',
        user='postgres',
        password='markim',
        port='5432'
    )
    return conn

@app.route("/")
def home():
    conn = db_conn()  # Conecta ao banco de dados
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users order by id")  # Executa uma consulta para obter todos os usuários
    data = cursor.fetchall()  # Busca todos os resultados da consulta
    cursor.close()
    conn.close()
    return render_template("index.html", data=data)
    #return render_template("index.html")  # Sua página inicial

@app.route("/create", methods=["POST"])
def index():
    conn = db_conn()
    cursor = conn.cursor()
    
    name = request.form["name"]  # Acessando o campo "name"

    query = f"INSERT INTO users (name) VALUES (%s)"
    cursor.execute(query, (name,))

        
    conn.commit()
    cursor.close()
    conn.close()
    
    #return redirect(url_for('home'))  # Redireciona para a página inicial
    return redirect(url_for("home"))

@app.route("/update", methods=["POST"])
def update_user():
    conn = db_conn()
    cursor = conn.cursor()
    user_id = request.form["id"]  # ID do usuário a ser atualizado
    new_name = request.form["name"]  # Novo nome para o usuário
    action = request.form['action']
    if action == "update":
        cursor.execute('''UPDATE users SET name = %s WHERE id = %s''', (new_name, user_id,))
        conn.commit()
    elif action == "delete":
        query = f"DELETE from users where id = %s"
        cursor.execute(query,(user_id,))
        #cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
     
    cursor.close()
    conn.close()
    
    return redirect(url_for('home')) 


@app.route("/api/index",methods = ["get"])
def api_index():
    
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("""Select * from users ORDER BY id ASC""")
    data = cursor.fetchall()
    return jsonify(data)

#@app.route("/api/edit/<resource_id>",methods = ["get"])
@app.route("/api/index/<resource_id>", methods=["GET"])
def api_edit(resource_id):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("""Select * from users WHERE ID = %s""",[resource_id])
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return jsonify(data)

@app.route("/api/create", methods=["POST"])
def api_create():
    new_request = request.get_json()
    conn = db_conn()
    cursor = conn.cursor()

    name = new_request["name"]
    cursor.execute("""INSERT INTO USERS (name) VALUES (%s)""",[name])
    conn.commit()
    cursor.close()
    return jsonify({"message":"criado com sucesso"})

@app.route("/api/update/<int:resource_id>", methods=["PUT"])
def api_update(resource_id):
    update_data = request.get_json()
    conn = db_conn()
    cursor = conn.cursor()

    name = update_data["name"]
    cursor.execute("""UPDATE USERS SET name = %s where id = %s""",[name,resource_id])
    conn.commit()
    cursor.close()
    return jsonify({"message":"criado com sucesso"})


@app.route("/api/delete/<int:resource_id>", methods=["DELETE"])
def api_deletar(resource_id):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM USERS WHERE ID = %s""",[resource_id])
    conn.commit()
    cursor.close()
    return jsonify({"message":"criado com sucesso"})




if __name__ == "__main__":
    app.run(debug=True,port=8000)



