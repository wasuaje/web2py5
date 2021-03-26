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
	mydiv.append(DIV(A(IMG(_src=URL('static/images','graficos.jpeg'), _alt="reportes ",  _width="80", _height="80", _class="none"),
										_href=URL('default','reportes')), CENTER(P(B("Reportes"))) , _class="img"))	

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
	mydiv.append(DIV(A(IMG(_src=URL('static/images','mesas.jpeg'), _alt="mesas",  _width="80", _height="80", _class="none"),
										_href=URL('mesas','index')), CENTER(P(B("Mesas"))) , _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','meseros2.jpg'), _alt="meseros",  _width="80", _height="80", _class="none"),
										_href=URL('meseros','index')), CENTER(P(B("Meseros"))) , _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','usuarios.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('ingrediente','index')), CENTER(P(B("Ingredientes"))) , _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('combro','index')), CENTER(P(B("Combos"))) , _class="imgmed"))	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('ingprod','index')), CENTER(P(B("Ingred por Prod"))) , _class="imgmed"))									
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('combro','index')), CENTER(P(B("Combos"))) , _class="imgmed"))	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('ingprod','index')), CENTER(P(B("Ingred por Prod"))) , _class="imgmed"))					
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('combro','index')), CENTER(P(B("Combos"))) , _class="imgmed"))	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','inventario.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="80", _height="80", _class="none"),
										_href=URL('ingprod','index')), CENTER(P(B("Ingred por Prod"))) , _class="imgmed"))					

	src="$('#modulos').show('slow');$('#modulos').width('550px');"
	mydiv2=DIV(DIV(H1(T("Productos y Categorias")), _class="title"),XML("".join(["%s" % (k) for k in mydiv])),SCRIPT(src))		
	return dict(mydiv=mydiv2)

def reportes():
	return dict()


def rptproducto():

	import subprocess
	import os	
	
	# Requerido si da errores de fuentes el jasperreport
	#sudo apt-get install msttcorefonts
	#
	

	#vieja manera de hacerlo
	#ruta='/home/wasuaje/Documentos/desarrollo/web2py5/applications'
	#reporter=ruta+URL('static/jasperstarter/bin','jasperstarter')	
	#report=ruta+URL('static/reports','productos.jasper')
	#reportgen=ruta+URL('static/rpts',session.user['usuario']+'-productos')

	#cambio reciente para trabajar en cualquier ruta
	reporter=os.path.join(request.folder,'static/jasperstarter/bin','jasperstarter')   
	
	report=os.path.join(request.folder,'static/reports','productos.jasper')   
	reportpdf=URL('static/rpts',session.user['usuario']+'-productos.pdf')
	
	reportgen=os.path.join(request.folder,'static/rpts',session.user['usuario']+'-productos')
	cmd='%s pr -t mysql -H localhost -u root -p www4214 -n dbPyRest -f pdf -i %s -o %s' % (reporter,report,reportgen)
	
	p = subprocess.check_call(cmd, shell=True)	
	redirect(reportpdf)
	#return dict(report=reportpdf)	

def rptproducto2():
# Let's import the wrapper
	import os
	import pdf
	from pdf.theme import colors, DefaultTheme

	# and define a constant
	TABLE_WIDTH = 540 # this you cannot do in rLab which is why I wrote the helper initially

    # then let's extend the Default theme. I need more space so I redefine the margins
    # also I don't want tables, etc to break across pages (allowSplitting = False)
    # see http://www.reportlab.com/docs/reportlab-userguide.pdf
	class MyTheme(DefaultTheme):
		doc = {
            'leftMargin': 25,
            'rightMargin': 25,
            'topMargin': 20,
            'bottomMargin': 25,
            'allowSplitting': False
            }
            
    # let's create the doc and specify title and author
	doc = pdf.Pdf('Productos 2', 'wuelfhis asuaje')

    # now we apply our theme
	doc.set_theme(MyTheme)

    # time to add the logo at the top right
	logo_path = os.path.join(request.folder,'static/images','facebook.png')   

	doc.add_image(logo_path, 67, 67, pdf.RIGHT)

    # give me some space
	doc.add_spacer()
    
    # this header defaults to H1
	doc.add_header('Productos - 2')

    # here's how to add a paragraph
	doc.add_paragraph("We are pleased to confirm your reservation with <b>%s</b>...")
	doc.add_spacer()	

	# let's move on to the divers table

	diver_table = [['Codigo', 'Nombre', 'Precio']] # this is the header row 

	for row in db(db.in_producto.id>0).select() :   
		diver_table.append([row.codigo, row.nombre, row.importe]) # these are the other rows

	doc.add_table(diver_table, TABLE_WIDTH)
	
	response.headers['Content-Type']='application/pdf'
	
	return doc.render()