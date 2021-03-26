# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():	
	tabla='cf_empresa'
	count =db(db[tabla].id > 0).count() 
	row=db(db[tabla].id > 0).select().first()
	if count > 0:
		registro=row.id
	else:
		registro = 0
	form = SQLFORM(db[tabla], registro,  submit_button='Enviar' ,    delete_label='Click para borrar:',  next=URL(c='empresa',  f='index'), \
			message=T("Operacion Exitosa !"),  upload=URL('download'))	
	if form.accepts(request.vars, session):
			response.flash = 'Operacion exitosa !'			
	elif form.errors:
			response.flash = 'Ha habido un error !'	
	return dict(myform=form)

def error():
    return dict()

def config():
	mydiv=[]	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','ico-inducom.png'), _alt="Empresa actual",  _width="120", _height="120", _class="none"),
										_href=URL('empresa','index')), CENTER(P(B("Empresa"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','parametro.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="120", _height="120", _class="none"),
										_href=URL('parametros','index')), CENTER(P(B("Parametros"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','usuarios.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="120", _height="120", _class="none"),
										_href=URL('usuarios','index')), CENTER(P(B("Usuarios/Accesos"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="120", _height="120", _class="none"),
										_href=URL('inventarios','index')), CENTER(P(B("Inventarios"))) , _class="img"))	
	mydiv2=DIV(DIV(H1(T("Modulos")), _class="title"),XML("".join(["%s" % (k) for k in mydiv])),   H2(P("Presione uno ...")))	
	
	return dict(mydiv=mydiv2)
