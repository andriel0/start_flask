from flask import render_template, request, flash, redirect, url_for
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user

lista_usuarios = ['andriel', 'alexandre', 'oliveira']


@app.route("/")
def home():
    return render_template('homepage.html')


@app.route("/contatos")
def contatos():
    return render_template('contatos.html')


@app.route("/usuarios")
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'btn_submit_login' in request.form:
        with app.app_context():
            usuario = Usuario.query.filter_by(email=form_login.email.data).first()
            if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                login_user(usuario, remember=form_login.lembrar_dados.data)
                flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
                return redirect(url_for('home'))
            else:
                flash(f'Email ou senha incorretos.', 'alert-danger')
    if form_criar_conta.validate_on_submit() and 'btn_submit_criar_conta' in request.form:
        with app.app_context():
            senha_cripto = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf8')
            usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data,
                              senha=senha_cripto)
            database.session.add(usuario)
            database.session.commit()
            flash(f'Conta criada com sucesso no e-mail {form_criar_conta.email.data}', 'alert-success')
            return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)