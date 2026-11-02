from flask import Blueprint, render_template, request, redirect, flash, session
from app.db import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        txt_user = request.form.get('username')
        txt_pass = request.form.get('password')

        usuario = Usuario.query.filter_by(username=txt_user).first()

        if usuario and usuario.password_hash == txt_pass:
            session['usuario_id'] = usuario.id
            session['username'] = usuario.username
            flash('¡Sesión iniciada correctamente!', 'success')
            return redirect('/')
        else:
            flash('Credenciales incorrectas.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'info')
    return redirect('/')
