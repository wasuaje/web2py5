# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

@auth.requires_membership('Operator') 
def index():   
	#elcrud=crud
	#elcrud.settings.download_url = URL('download')
    if  request.args(0) <> None :
        tabla=request.args(0)
        registro=db[request.args(0)](request.args(1))		
        labels={'mt_persona_id':'Persona', 'cf_cargo_id':'Cargo', 'cf_tipo_doc_id':'Tipo Doc', 'mt_vehiculo_id':'Placa', 
          'mt_estado_id':'Estado'
          }
        #form = elcrud.create(db[tabla], next=URL('index/'+tabla), message=T("Registro insertado con exito"), labels=labels)
        form = SQLFORM(db[tabla], registro,  submit_button='Enviar' ,    delete_label='Click para borrar:',  next=URL(c='maestros',  f='index/'+tabla), \
            message=T("Operacion Exitosa !"), labels=labels, upload=URL('download'))	
        if 'ciudad' in tabla:
            lista = db(db.mt_ciudad.mt_estado_id==db.mt_estado.id).select()
            tipo='listciudad'
        elif 'mt_estado' in tabla:
			lista = db(db.mt_estado).select()
			tipo='listestado'									
        elif 'mt_persona' in tabla:
			lista = db(db.mt_persona.cf_cargo_id==db.cf_cargo.id).select()
			tipo='listper'
        elif 'mt_doc_' in tabla:
			lista = db(db[tabla]).select()
			tipo='listdocs'			
        elif 'mt_vehiculo' in tabla:
			lista = db((db.mt_vehiculo.cf_vehiculo_modelo_id==db.cf_vehiculo_modelo.id) & (db.cf_vehiculo_modelo.cf_vehiculo_marca_id==db.cf_vehiculo_marca.id)).select()			
			tipo='listaveh' 			
        elif 'cf_empresa' in tabla:
			lista = db(db.cf_empresa).select()
			tipo = 'listaemp'
        elif 'mt_kilometraje' in tabla:
			lista = db(db.mt_kilometraje.mt_vehiculo_id==db.mt_vehiculo.id).select()
			tipo = 'listakilo'
        elif 	'proveedor' in tabla:
            lista = db(db.cf_proveedor).select()
            tipo = 'proveedor'	
            #print lista
					
        if form.accepts(request.vars, session):
			response.flash = 'Operacion exitosa !'
			redirect(URL(c='maestros',  f='index/'+tabla))
        elif form.errors:
			response.flash = 'Ha habido un error !'		
        return dict(form=form, lista=lista, tabla=tabla, tipo=tipo)		
    else:
        return dict(message='Listados Maestros', tablas=db.tables)

	

#	elif request.args(0) <> None and request.args(1) <> None:	  	
#tabla=request.args(0)
#   	  registro=request.args(1)
#  	  form = elcrud.update(db[tabla], registro, next=URL('index/'+tabla),  message=T("Registro actualizado con exito"))
 #  	  return dict(message='Listado Maestros', form=form,  tabla=tabla)

	

def download():
	return response.download(request, db)    

def listado():
	response.title = "Listado de Ejemplo"
    
    # define header and footers:
	head = THEAD(TR(TH("Cedula",_width="50%"), 
                    TH("Nombres",_width="30%"),
                    TH("Apellidos",_width="20%"), 
                    _bgcolor="#585858"))
	foot = TFOOT(TR(TH("",_width="50%"), 
                    TH("",_width="30%"),
                    TH("",_width="20%"),
                    _bgcolor=""))
    
    # create several rows:
	rows = []
	lineas=db(db.mt_persona).select(orderby=db.mt_persona.cedula)	
	col = 0
	for i in lineas:		
		col=col+1
		#bak = col % 2 and "#F0F0F0" or "#FFFFFF"
		bak = col % 2 and "#BDBDBD" or ""				
		rows.append(TR(TD(i.cedula),
                       TD(i.nombres, _align="center"),
						TD(i.apellidos, _align="right"),
						_bgcolor=bak)) 		
    # make the table object
	body = TBODY(*rows)
	table = TABLE(*[head,foot, body], 
                  _border="1", _align="center", _width="100%")

	if request.extension=="pdf":
		from gluon.contrib.pyfpdf import FPDF, HTMLMixin

        # define our FPDF class (move to modules if it is reused  frequently)
		class MyFPDF(FPDF, HTMLMixin):
			def header(self):
				self.set_font('Arial','B',15)
				self.cell(0,10, response.title ,1,0,'C')
				self.ln(20)
			def footer(self):
				self.set_y(-15)
				self.set_font('Arial','I',8)
				txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
				self.cell(0,10,txt,0,0,'C')
                    
		pdf=MyFPDF()
		# first page:
		pdf.add_page()
		pdf.write_html(str(XML(table, sanitize=False)))
		response.headers['Content-Type']='application/pdf'
		return pdf.output(dest='S')
	else:
        # normal html view:
		return dict(table=table)

def vehiculo_report():
	from reports import ReportVehiculo
	from geraldo.generators import PDFGenerator
	import gluon.contenttype
	import StringIO
	resp = StringIO.StringIO()
	vehiculos = db(db.mt_vehiculo.id > 0).select(orderby=db.mt_vehiculo.placa)
	report = ReportVehiculo(queryset=vehiculos)
	report.generate_by(PDFGenerator, filename=resp)
	resp.seek(0)
	response.headers['Content-Type'] = gluon.contenttype.contenttype('.pdf')
	filename = "%s_Vehiculos.pdf" % (request.env.server_name)
	response.headers['Content-disposition'] = "attachment; filename=\"%s\"" % filename
	return resp.read()
    
    
    
    
    
    
    
    
