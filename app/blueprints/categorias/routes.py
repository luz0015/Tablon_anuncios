from flask import Blueprint, render_template, request, redirect, flash
from app.db import db, Categoria

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        txt_nombre = request.form.get('nombre')
        txt_descripcion = request.form.get('descripcion')

        existe = Categoria.query.filter_by(nombre=txt_nombre).first()
        if existe:
            flash('La categoría ya existe.', 'warning')
        else:
            nueva = Categoria(nombre=txt_nombre, descripcion=txt_descripcion)
            db.session.add(nueva)
            db.session.commit()
            flash('Categoría añadida de forma correcta.', 'success')
        return redirect('/categorias')

    lista_categorias = Categoria.query.all()
    return render_template('categorias/index.html', categorias=lista_categorias)


@categorias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    c = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        c.nombre = request.form.get('nombre')
        c.descripcion = request.form.get('descripcion')
        db.session.commit()
        flash('Categoría modificada.', 'success')
        return redirect('/categorias')
    return render_template('categorias/editar.html', categoria=c)

@categorias_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    c = Categoria.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash('Categoría eliminada del sistema.', 'info')
    return redirect('/categorias')
