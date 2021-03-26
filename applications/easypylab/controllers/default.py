# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
	""" 
	Seteo todas las variables de sesion iniciales que se mantendran por todo el el sistema y 
	que son de utilidad en multiples ocasiones. Empresa, usuarios, configuraciones por ejemplo
	"""
	#Query a la empresa y al usuario para obtener estos valores.
	mensaje=''
	session.empresa  = session.empresa or {}
	session.user  = session.user or {}
	crow=db(db.cf_empresa.id > 0).select()
	crow=len(crow)
	if crow>0:
		row= db(db.cf_empresa.id > 0).select().first()	
		session.empresa['id']=row.id
		session.empresa['nombre']=row.nombre
		session.empresa['razon']=row.razon_social
		session.empresa['rif']=row.rif
		session.empresa['nit']=row.nit
		session.empresa['email']=row.email
		session.empresa['direccion']=row.direccion
		session.empresa['telefono']=row.tlf
		session.empresa['ruta_foto']=row.ruta_foto
	
		#print session.empresa
		"""session.user[id]
		session.user[nombre]
		session.user[usuario]#"""
		session.user['usuario']='wasuaje'
	else:
		mensaje+="Configure la empresa 01 - "		
	
	prow=db(db.cf_parametro.id > 0).select()
	prow=len(prow)	
	if prow>0:
		pass
	else:		
		mensaje+="Configure al menos los parametros basicos - "

	response.flash=T(mensaje)
	return dict()

def error():
    return dict()

def modulos():
	mydiv=[]	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','sistema.jpg'), _alt="Punto de venta, POS",  _width="80", _height="80", _class="none"),
										_href=URL('pos','index')), CENTER(P(B("Punto de Venta"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','meseros.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('configserv','index')), CENTER(P(B("Configurar servicio"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','meseros.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('configserv','index')), CENTER(P(B("Configurar servicio"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','meseros.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('configserv','index')), CENTER(P(B("Configurar servicio"))) , _class="img"))	
	
	src="$('#modulos').show('slow');$('#modulos').width('550px');"
	mydiv2=DIV(DIV(H1(T("Modulos")), _class="title"),XML("".join(["%s" % (k) for k in mydiv])) , SCRIPT(src))
	
	  
	return dict(mods=mydiv2)

def config():
	mydiv=[]	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','ico-inducom.png'), _alt="Empresa actual",  _width="80", _height="80", _class="none"),
										_href=URL('empresa','index')), CENTER(P(B("Empresa"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','parametro.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('parametros','index')), CENTER(P(B("Parametros"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','usuarios.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('usuarios','index')), CENTER(P(B("User/Acces."))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('inventarios','index')), CENTER(P(B("Inventarios"))) , _class="img"))		

	src="$('#modulos').show('slow');$('#modulos').width('550px');"
	
	mydiv2=DIV(DIV(H1(T("Configuracion")), _class="title"),XML("".join(["%s" % (k) for k in mydiv])),  SCRIPT(src))
	
	
	return dict(mydiv=mydiv2,)

def configprod():
	mydiv=[]	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','ico-inducom.png'), _alt="Empresa actual",  _width="120", _height="120", _class="none"),
										_href=URL('categoria','index')), CENTER(P(B("Categorias"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','parametro.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="120", _height="120", _class="none"),
										_href=URL('producto','index')), CENTER(P(B("Productos"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','usuarios.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="120", _height="120", _class="none"),
										_href=URL('ingrediente','index')), CENTER(P(B("Ingredientes"))) , _class="img"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="120", _height="120", _class="none"),
										_href=URL('combro','index')), CENTER(P(B("Combos"))) , _class="img"))	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="120", _height="120", _class="none"),
										_href=URL('ingprod','index')), CENTER(P(B("Ingred por Prod"))) , _class="img"))											
	

	src="$('#modulos').show('slow');$('#modulos').width('550px');"
	mydiv2=DIV(DIV(H1(T("Productos y Categorias")), _class="title"),XML("".join(["%s" % (k) for k in mydiv])),SCRIPT(src))	
	

	return dict(mydiv=mydiv2)

def maestra():
	mydiv=[]	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','examenes.png'), _alt="mesas",  _width="80", _height="80", _class="none"),
										_href=URL('examen','index')), CENTER(P(B("Examentes"))) , _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','determinaciones.png'), _alt="meseros",  _width="80", _height="80", _class="none"),
										_href=URL('determin','index')), CENTER(P(B("Determinac."))) , _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','config2.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('perfil','index')), CENTER(P(B("Perfiles"))) , _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','unidades.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('valor','index')), CENTER(P(B("Valores Nor."))) , _class="imgmed"))	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('ingprod','index')), CENTER(P(B("Ingred Prod"))) , _class="imgmed"))									
	

	src="$('#modulos').show('slow');$('#modulos').width('550px');"
	mydiv2=DIV(DIV(H1(T("Productos y Categorias")), _class="title"),XML("".join(["%s" % (k) for k in mydiv])),SCRIPT(src))		
	return dict(mydiv=mydiv2)

def reportes():
	return dict()


def rptproducto():

	import subprocess
	ruta='/home/wasuaje/Documentos/desarrollo/web2py5/applications'
	reporter=ruta+URL('static/jasperstarter/bin','jasperstarter')
	report=ruta+URL('static/reports','productos.jasper')
	reportpdf=URL('static/rpts',session.user['usuario']+'-productos.pdf')
	reportgen=ruta+URL('static/rpts',session.user['usuario']+'-productos')
	cmd='%s pr -t mysql -H localhost -u root -p www4214 -n dbPyRest -f pdf -i %s -o %s' % (reporter,report,reportgen)
	#&& evince %s
	#print cmd
	#p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	p = subprocess.check_call(cmd, shell=True)
	#print "p",type(p)
	#p=1	
	redirect(reportpdf)
	#return dict(report=reportpdf)	


def pruebadropdown():
    """query = ....
    db.table.field.requires=IS_IN_DB(db(query),....)
    form=SQLFORM(...)
    if form.accepts(...)
        ...
    return dict(form=form)
	"""

