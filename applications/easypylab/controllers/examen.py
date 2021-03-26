# -*- coding: utf-8 -*-
### required - do no delete
import json
import math 

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():		
	myform=FORM(TABLE(TR(B('Cod.'),B('Nombre'),B('P.Unit'),B('P.Seg.'),B('P.Emp'),B('PE1'),B('PE2')),
					TR(INPUT(_type='text', _id='codigo',_name='codigo',_style='width:30px'),
					   INPUT(_type='text', _id='nombre',_name='nombre',_style='width:120px'),
					 INPUT(_type='text', _id='punit',_name='punit',_style='width:30px'),  
					 INPUT(_type='text', _id='pseg',_name='pseg',_style='width:30px'),
					 INPUT(_type='text', _id='pemp',_name='pemp',_style='width:30px'),
					 INPUT(_type='text', _id='pe1',_name='pe1',_style='width:30px'),
					 INPUT(_type='text', _id='pe2',_name='pe2',_style='width:30px'),
					INPUT(_type='button',_value='+',_id='ad',_name='ad',_onclick="ajax('subhandle', \
											['codigo','nombre','punit','pseg','pemp','pe1','pe2','ad'],'result')"),
					INPUT(_type='button',_value='-',_id='del',_name='del')
					  )	\
				     ) \
			   )
		
	

	return dict(myform=myform)

def handle():
	tabla='cf_examen'
	
	if len(request.args) > 0:
		id = request.args[0]
		row=db(db[tabla].id == id).select().first()
		registro=row.id
	else:
		registro = 0
	form = SQLFORM(db[tabla], registro, deletable=True,  submit_button='Enviar' ,    delete_label='Click para borrar:',  next=URL(c='examen',  f='handle'), \
			message=T("Operacion Exitosa !"),  upload=URL('download'))	
	if form.accepts(request.vars, session):
			response.flash = 'Operacion exitosa !'			
	elif form.errors:
			response.flash = 'Ha habido un error !'	
	return dict(myform=form)	

def subhandle():	
	scr="""			
		$("#list10").trigger("reloadGrid"); 
		jQuery('#codigo').val('');     											
		jQuery('#nombre').val('');
		jQuery('#punit').val('');     											
		jQuery('#pseg').val('');
		jQuery('#pemp').val('');     											
		jQuery('#pe1').val('');
		jQuery('#pe2').val('');		
		""" 
	codigo=request.vars.codigo
	nombre=request.vars.nombre
	punit=request.vars.punit
	pseg=request.vars.pseg
	pemp=request.vars.pemp
	pe1=request.vars.pe1
	pe2=request.vars.pe2
	ex_id=request.vars.id_examen
	
	if request.vars.action=='del':
		examen_id=db(db.cf_examen.id==ex_id).delete()		          
		if examen_id > 0:
			mensaje="Registro eliminado con exito"
		else:
			mensaje="Ha habido un error eliminando"
	else:
		examen_id=db.cf_examen.insert(codigo=codigo,nombre=nombre,precio_fin=punit,precio_seg=pseg, \
								precio_emp=pemp,precio_esp1=pe1,precio_esp2=pe2)		
		if examen_id > 0:
			mensaje="Registro insertado con exito"
		else:
			mensaje="Ha habido un error insertando"

	return dict(a=DIV(T(mensaje),  SCRIPT(scr)))

def error():
    return dict()
def getdata():
	tabla='cf_examen'
	searching=False
	page = request.vars.page #// get the requested page 
	limit = request.vars.rows  #// get how many rows we want to have into the grid 
	limitini = int(request.vars.rows) #// get how many rows we want to have into the grid 
	sidx =  request.vars.sidx #// get index row - i.e. user click to sort $sord = nombre
	sord =  request.vars.sord  #// get the direction asc or desc
	
	if request.vars.searchField:
		searching=True
		searchopt=request.vars.searchOper
		searchfield=request.vars.searchField
		searchstring=request.vars.searchString		
		searchquery=search(tabla, searchopt, searchfield,searchstring )

	if not page:
		page = 1
	else:
		page=int(page)
		
	if not limit:
		limit = 10
	else:		
		limit=int(limit)
		
	if not sidx:
		sidx =1 # // connect to the database 

	count =db(db[tabla].id > 0).count() 
	if  count > 0:
		total_pages = int(math.ceil(float(count)/float(limit)))
	else:		
		total_pages = 0
		
	#print total_pages	
	
	if page >= total_pages:		
		page=total_pages
		limit=count		
		start = limitini*page - limitini # // do not put $limit*($page - 1)		
	else:		
		limit=limit*page
		#start = limit*page - limit # // do not put $limit*($page - 1)
		start = limit-limitini # // do not put $limit*($page - 1)
	if limit < 0 :		
		limit = 0		
	
	if start < 0  :
		start = 0;	
	#print "start", start	
	#print "limit", limit
	resp={}
	resp={'page':page,'total':total_pages,'records':count,'rows':[]}
	#for row in db(db.in_categoria.id > 0).select():
	if sord=='asc':
		orderby=db[tabla][sidx]
	else:
		orderby=~db[tabla][sidx]

	if searching:
		query=db( (eval(searchquery)) & (db[tabla].id > 0) & (db[tabla].es_perfil == None) & (db[tabla].examen_id == None)  ).select()
	else:				
		query=db( (db[tabla].id > 0) & (  db[tabla].es_perfil == None ) & (db[tabla].examen_id == None) ).select( limitby=( start, limit) , orderby=orderby )
		
	for row in query:
	#for row in  db(db.fc_cobro.cf_proveedor_id==db.cf_proveedor.id).select():
		rw={}
		rw['id']=row.id
		rw['cell']=[row.id,row.codigo,row.nombre,row.precio_fin,row.precio_seg,row.precio_emp,row.precio_esp1,row.precio_esp2]
		resp['rows'].append(rw)

	data=json.dumps(resp)
	return data

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

def search(tabla, searchopt, searchfield,searchstring):
	#bw - begins with ( LIKE val% )
#eq - equal ( = )
#ne - not equal ( <> )
#lt - little ( < )
#le - little or equal ( <= )
#gt - greater ( > )
#ge - greater or equal ( >= )
#ew - ends with (LIKE %val )
#cn - contain (LIKE %val% )		
	if searchopt == 'eq':
		searchopt='=='
	elif searchopt == 'ne':
		searchopt='<>'
	elif searchopt == 'lt':
		searchopt='<'
	elif searchopt == 'gt':
		searchopt='>'
	elif searchopt == 'le':
		searchopt='<='
	elif searchopt == 'ge':
		searchopt='>='		
	elif searchopt == 'bw':
		searchpt=".like(%(field)r)" % {'field':searchstring+'%'}		
	elif searchopt == 'ew':
		searchpt=".like(%(field)r)" % {'field':'%'+searchstring}
	elif searchopt == 'cn':
		searchpt=".like(%(field)r)" % {'field':'%'+searchstring+'%'}
	#para que solo tome los id como entero todo lo demas es un string
	if searchfield=='id':
		if searchopt in "bw ew cn":
			searchquery=''
		else:
			 searchquery='db.'+tabla+'.'+searchfield+searchopt+searchstring 
	else:
		if searchopt in "bw ew cn":
			searchquery='db.'+tabla+'.'+searchfield+searchpt
		else:
			searchquery='db.'+tabla+'.'+searchfield+searchopt+"'"+searchstring+"'"	
	return searchquery
	
	
