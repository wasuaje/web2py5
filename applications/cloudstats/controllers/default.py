# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
	"""
	example action using the internationalization operator T and flash
	rendered by views/default/index.html or views/generic.html
	if you need a simple wiki simple replace the two lines below with:
	return auth.wiki()
	"""
	import os
	import sys

	try:
		import cPickle as pickle
	except ImportError:
		import pickle
	
	import urllib
	#from gluon.serializers import json
	import simplejson as json
	import datetime
	response.flash = T("Bienvenidos !")
	urlbase='https://www.cloudflare.com/api_json.html'
	tkn='323959e52c12fffcde6433413c5e5c0b7e0f2'
	email='sistemas-internet@eluniversal.com'
	z='eluniversal.com'
	
	form = SQLFORM.factory(
	Field('filename',label=T('Nombre de archivo a purgar: http://cdn.eluniversal.com/'), requires=IS_NOT_EMPTY())
	)

	if form.process().accepted:
		#formulario para limpiar cache de archivo especifico
		filename = form.vars.filename		
		a='zone_file_purge'
		url='http://www.eluniversal.com/%s' % filename
		params = urllib.urlencode({'a':a,'tkn': tkn, 'email': email, 'z': z, 'url':url})
		f = urllib.urlopen(urlbase+"/?%s" % params)
		f=json.loads(f.read())
		h=f["result"]
		m=f["msg"]
		#print f
		if h=="success":
			response.flash = 'Archivo purgado !'			
		else:
			response.flash = 'Error: %s' % m 
	elif form.errors:
		response.flash = 'No puede estar en blanco'
	
#Solicito la data estadistica a la fecha de cloudflare
	a='stats'
	interval='120'
	params = urllib.urlencode({'a':a,'tkn': tkn, 'email': email, 'z': z, 'interval':interval})
	f = urllib.urlopen(urlbase+"/?%s" % params)
	f=json.loads(f.read())
	
	#print f['response']['result']
	h= f['response']['result']['objs'][0]['currentServerTime']
	zoncdate= datetime.datetime.fromtimestamp(h / 1e3)	
	trafic={}
	
	trafic['uniq']={'Regular':f['response']['result']['objs'][0]['trafficBreakdown']['uniques']['regular'],
							'Threat':f['response']['result']['objs'][0]['trafficBreakdown']['uniques']['threat'],
							'Crawler':f['response']['result']['objs'][0]['trafficBreakdown']['uniques']['crawler'] }
	trafic['pages']={'Regular':f['response']['result']['objs'][0]['trafficBreakdown']['pageviews']['regular'],
							'Threat':f['response']['result']['objs'][0]['trafficBreakdown']['pageviews']['threat'],
							'Crawler':f['response']['result']['objs'][0]['trafficBreakdown']['pageviews']['crawler'] }					    
	trafic['served']={'Cloudflare':f['response']['result']['objs'][0]['requestsServed']['cloudflare'], 
								'User':f['response']['result']['objs'][0]['requestsServed']['user']
	                  }
	trafic['band']={'Cloudflare':f['response']['result']['objs'][0]['bandwidthServed']['cloudflare']/1024,
								'User':f['response']['result']['objs'][0]['bandwidthServed']['user']/1024
	                }
	#print  trafic

########################google chart##################
	fichero = file('/home/wasuaje/Documentos/desarrollo/web2py5/applications/cloudstats/static/images/data.dat')
	data = pickle.load(fichero)	
	fichero.close()
	c=[]
	c.append(['X','Hits'])
	for i in range( len(data['data'])-12, len(data['data'])):
		c.append([data['label'][i].isoformat(),data['data'][i]])
		
	scp1="""google.load('visualization', '1', {packages: ['corechart']}); 
			      google.load('barhit', '1', {packages: ['corechart']});	
				  google.load('paghit', '1', {packages: ['corechart']});	
				  google.load('serhit', '1', {packages: ['corechart']});					  
				  google.load('serban', '1', {packages: ['corechart']});					  
			"""
		
	scp2="""
		function drawVisualization() {
		// Create and populate the data table.
		var data = google.visualization.arrayToDataTable( %s );
	
		// Create and draw the visualization.
		new google.visualization.LineChart(document.getElementById('visualization')).
			draw(data, {title:"Historico visitantes unicos",curveType: "function",
						width: 900, height: 400,
						vAxis: {maxValue: 10}}
				);
		}
      google.setOnLoadCallback(drawVisualization);    
	""" % c
			
#bar hits
	d=[]
	d.append(['Tipos','Hits'])
	for i in trafic['uniq'].keys():
		d.append([i, trafic['uniq'][i]])
	scp3="""function drawbarhit() {
        // Create and populate the data table.
        var data = google.visualization.arrayToDataTable( %s );
      
        // Create and draw the visualization.
        new google.visualization.PieChart(document.getElementById('barhit')).
            draw(data, {title:"Trafico Unico",width: 400, height: 300});
      }
	 google.setOnLoadCallback(drawbarhit);    
   """ % d

#barpages
	e=[]
	e.append(['Tipos','Hits'])
	for i in trafic['pages'].keys():
		e.append([i, trafic['pages'][i]])
	scp4="""function drawpaghit() {
        // Create and populate the data table.
        var data = google.visualization.arrayToDataTable( %s );
      
        // Create and draw the visualization.
        new google.visualization.PieChart(document.getElementById('paghit')).
            draw(data, {title:"Paginas Vistas",width: 400, height: 300});
      }
	 google.setOnLoadCallback(drawpaghit);    
   """ % e

#barserved
	f=[]
	f.append(['Tipos','Hits'])
	for i in trafic['served'].keys():
		f.append([i, trafic['served'][i]])
	scp5="""function drawserhit() {
	  // Create and populate the data table.
        var data = google.visualization.arrayToDataTable( %s );
      
        // Create and draw the visualization.
        new google.visualization.PieChart(document.getElementById('serhit')).
            draw(data, {title:"Request Servidos por",width: 400, height: 300});
	}
	google.setOnLoadCallback(drawserhit);    
	""" % f
	
#barband
	g=[]
	g.append(['Tipos','Hits'])
	for i in trafic['band'].keys():
		g.append([i, trafic['band'][i]/1024])
	scp6="""function drawbanhit() {
	  // Create and populate the data table.
        var data = google.visualization.arrayToDataTable( %s );
      
        // Create and draw the visualization.
        new google.visualization.PieChart(document.getElementById('serban')).
            draw(data, {title:"GB Servidos por",width: 400, height: 300});
	}
	google.setOnLoadCallback(drawbanhit);    
	""" % g
	
	div1=DIV(_id="visualization" , _style="width: 900px; height: 400px; "  )
	div2=DIV(_id="barhit" , _style="width: 300px; height: 300px;" , _class='mydiv'  )
	div3=DIV(_id="paghit" , _style="width: 300px; height: 300px;"  , _class='mydiv'  )
	div4=DIV(_id="serhit" , _style="width: 300px; height: 300px;"  , _class='mydiv'  )	
	div5=DIV(_id="serban" , _style="width: 300px; height: 300px;"  , _class='mydiv'  )	
	

	
	scp1=SCRIPT(scp1, _type="text/javascript")
	scp2=SCRIPT(scp2, _type="text/javascript")
	scp3=SCRIPT(scp3, _type="text/javascript")
	scp4=SCRIPT(scp4, _type="text/javascript")
	scp5=SCRIPT(scp5, _type="text/javascript")
	scp6=SCRIPT(scp6, _type="text/javascript")
	
	mydiv=DIV(div1, div2, div3, div4, div5)

	return dict( f=mydiv, scp1=scp1, scp2=scp2, scp3=scp3, scp4=scp4, scp5=scp5,scp6=scp6, form=form)
def test():
    return dict(name=CAT(B("Menu "), request.vars.name))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
