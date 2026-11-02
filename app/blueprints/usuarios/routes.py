from flask import Blueprint, render_template, request, redirect, flash, session
from app.db import db, Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        txt_username = request.form.get('username')
        txt_email = request.form.get('email')
        txt_password = request.form.get('password')

        existe = Usuario.query.filter_by(username=txt_username).first()
        if existe:
            flash('El nombre de usuario ya está en uso.', 'danger')
        else:
            nuevo = Usuario(username=txt_username, email=txt_email, password_hash=txt_password)
            db.session.add(nuevo)
            db.session.commit()
            flash('Usuario creado con éxito.', 'success')
        return redirect('/usuarios')

    lista_usuarios = Usuario.query.all()
    return render_template('usuarios/index.html', usuarios=lista_usuarios)
@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    u = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        u.username = request.form.get('username')
        u.email = request.form.get('email')
        if request.form.get('password'):
            u.password_hash = request.form.get('password')
        db.session.commit()
        flash('Usuario modificado con éxito.', 'success')
        return redirect('/usuarios')
    return render_template('usuarios/editar.html', usuario=u)

@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    u = Usuario.query.get_or_404(id)
    if session.get('usuario_id') == u.id:
        session.clear() 
    db.session.delete(u)
    db.session.commit()
    flash('Usuario eliminado.', 'info')
    return redirect('/usuarios')
