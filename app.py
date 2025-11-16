from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt
import time
import uuid
from utils import load_users, save_users, now_ts

app = Flask(__name__)
app.secret_key = "troque_esta_chave_por_uma_secreta_em_producao"

USERS_FILE = "user.json"

# Configurações do sistema
MAX_FAILED = 5           # número de tentativas antes do bloqueio
LOCK_SECONDS = 5 * 60    # bloqueio por 5 minutos
RECOVERY_TOKEN_TTL = 15 * 60  # token de recuperação válido por 15 minutos

@app.route("/")
def index():
    if session.get("username"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET","POST"])
def register():
    users = load_users(USERS_FILE)
    if request.method == "POST":
        username = request.form.get("username","").strip().lower()
        password = request.form.get("password","")
        if not username or not password:
            flash("Preencha usuário e senha")
            return redirect(url_for("register"))
        if len(password) < 6:
            flash("Senha deve ter pelo menos 6 caracteres")
            return redirect(url_for("register"))
        if username in users:
            flash("Usuário já existe")
            return redirect(url_for("register"))

        # cria hash com bcrypt
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        users[username] = {
            "password": hashed.decode(),     # armazenamos como str
            "failed": 0,
            "locked_until": 0,
            "recovery": None
        }
        save_users(USERS_FILE, users)
        flash("Registrado com sucesso. Faça login.")
        return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/login", methods=["GET","POST"])
def login():
    users = load_users(USERS_FILE)
    if request.method == "POST":
        username = request.form.get("username","").strip().lower()
        password = request.form.get("password","")
        user = users.get(username)
        if not user:
            flash("Usuário ou senha inválidos")
            return redirect(url_for("login"))

        # verifica se está bloqueado
        if user.get("locked_until",0) > now_ts():
            wait = int(user["locked_until"] - now_ts())
            flash(f"Conta bloqueada. Tente novamente em {wait} segundos.")
            return redirect(url_for("login"))

        stored_hash = user["password"].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            # sucesso: reset de tentativas
            user["failed"] = 0
            user["locked_until"] = 0
            user["recovery"] = None
            save_users(USERS_FILE, users)
            session["username"] = username
            flash("Login efetuado")
            return redirect(url_for("dashboard"))
        else:
            # falha de autenticação
            user["failed"] = user.get("failed",0) + 1
            if user["failed"] >= MAX_FAILED:
                user["locked_until"] = now_ts() + LOCK_SECONDS
                flash(f"Muitas tentativas. Conta bloqueada por {LOCK_SECONDS} segundos.")
            else:
                flash(f"Usuário ou senha inválidos. Tentativas: {user['failed']}/{MAX_FAILED}")
            save_users(USERS_FILE, users)
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Desconectado")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if not session.get("username"):
        flash("Faça login primeiro")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

# Recuperação simulada - solicita token
@app.route("/recover", methods=["GET","POST"])
def recover_request():
    users = load_users(USERS_FILE)
    if request.method == "POST":
        username = request.form.get("username","").strip().lower()
        user = users.get(username)
        if not user:
            flash("Se o usuário existir, um token foi enviado (simulado).")
            return redirect(url_for("login"))
        token = str(uuid.uuid4())
        expire = now_ts() + RECOVERY_TOKEN_TTL
        user["recovery"] = {"token": token, "expires": expire}
        save_users(USERS_FILE, users)
        # Simulação de envio (no mundo real, enviar por email)
        print(f"[SIMULADO] Token de recuperação para {username}: {token}")
        flash("Token de recuperação gerado e 'enviado' (veja console).")
        return redirect(url_for("recover_confirm"))
    return render_template("recuperar-solicitção.html")

# Confirma token e altera senha
@app.route("/recover/confirm", methods=["GET","POST"])
def recover_confirm():
    users = load_users(USERS_FILE)
    if request.method == "POST":
        username = request.form.get("username","").strip().lower()
        token = request.form.get("token","").strip()
        newpass = request.form.get("newpass","")
        if not username or not token or not newpass:
            flash("Preencha todos os campos")
            return redirect(url_for("recover_confirm"))
        if len(newpass) < 6:
            flash("Nova senha deve ter pelo menos 6 caracteres")
            return redirect(url_for("recover_confirm"))
        user = users.get(username)
        if not user or not user.get("recovery"):
            flash("Token inválido ou usuário desconhecido")
            return redirect(url_for("recover_confirm"))
        rec = user["recovery"]
        if rec["token"] != token or now_ts() > rec["expires"]:
            flash("Token inválido ou expirado")
            return redirect(url_for("recover_confirm"))
        # altera senha
        hashed = bcrypt.hashpw(newpass.encode(), bcrypt.gensalt())
        user["password"] = hashed.decode()
        user["failed"] = 0
        user["locked_until"] = 0
        user["recovery"] = None
        save_users(USERS_FILE, users)
        flash("Senha alterada com sucesso. Faça login.")
        return redirect(url_for("login"))
    return render_template("recuperar-confirmação.html")

if __name__ == "__main__":
    app.run(debug=True)
