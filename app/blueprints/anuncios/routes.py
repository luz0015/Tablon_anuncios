from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from app.db import db, Anuncio, Categoria

anuncios_bp = Blueprint('anuncios', __name__)

@anuncios_bp.route('/')
def index():
    lista_anuncios = Anuncio.query.order_by(Anuncio.fecha_creacion.desc()).all()
    return render_template('anuncios/index.html', anuncios=lista_anuncios)

@anuncios_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para publicar un anuncio.', 'danger')
        return redirect('/auth/login')

    nombres_fijos = ["General", "Interno", "Otro"]
    for nombre in nombres_fijos:
       
        existe = Categoria.query.filter_by(nombre=nombre).first()
        if not existe:
            nueva_cat = Categoria(nombre=nombre)
            db.session.add(nueva_cat)
    db.session.commit() 
    if request.method == 'POST':
       
        ids_categorias = request.form.getlist('categoria_id[]')
        
       
        id_cat_seleccionado = int(ids_categorias[0]) if ids_categorias and ids_categorias[0] else None

        nuevo_anuncio = Anuncio(
            titulo=request.form.get('titulo'),
            contenido=request.form.get('contenido'),
            categoria_id=id_cat_seleccionado,
            usuario_id=session['usuario_id']
        )
        
        try:
            db.session.add(nuevo_anuncio)
            db.session.commit()
            flash('¡Anuncio colgado!', 'success')
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            print("Error al guardar el anuncio:", e)
            flash('Ocurrió un error al guardar el anuncio.', 'danger')

    opciones_categorias = Categoria.query.all()
    return render_template('anuncios/nuevo.html', categorias=opciones_categorias)

# Modificar anuncio
@anuncios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    a = Anuncio.query.get_or_404(id)
    if 'usuario_id' not in session or a.usuario_id != session['usuario_id']:
        flash('No tienes permiso para modificar este anuncio.', 'danger')
        return redirect('/')

    if request.method == 'POST':
        a.titulo = request.form.get('titulo')
        a.contenido = request.form.get('contenido')
        
        ids_categorias = request.form.getlist('categoria_id[]')
        id_cat_seleccionado = int(ids_categorias[0]) if ids_categorias and ids_categorias[0] else None
        
        a.categoria_id = id_cat_seleccionado
        db.session.commit()
        flash('Anuncio actualizado.', 'success')
        return redirect('/')

    opciones_categorias = Categoria.query.all()
    return render_template('anuncios/editar.html', anuncio=a, categorias=opciones_categorias)


@anuncios_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    if 'usuario_id' not in session:
        return redirect('/auth/login')
    a = Anuncio.query.get_or_404(id)
    if a.usuario_id == session['usuario_id']:
        db.session.delete(a)
        db.session.commit()
        flash('Anuncio eliminado.', 'info')
    return redirect('/')

