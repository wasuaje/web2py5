from geraldo import Report, ReportBand, DetailBand, SystemField, Label, ObjectValue, ReportGroup
from reportlab.lib.pagesizes import A4

from geraldo.utils import cm, BAND_WIDTH, TA_CENTER, TA_RIGHT

class ReportVehiculo(Report):

	title = 'Vehiculos'
	author = 'Wuelfhis Asuaje'
	page_size = A4
	margin_left = 2*cm
	margin_top = 2*cm
	margin_right = 2*cm
	margin_bottom = 2*cm

	class band_page_header(ReportBand):
		height = 1.0*cm
		elements = [
			SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            Label(text="Id", top=1.5*cm, left=0.5*cm),
            Label(text="Placa", top=1.5*cm, left=3*cm),
			]
		borders = {'all': True}

	class band_detail(ReportBand):
		height = 0.5*cm
		elements=(
            ObjectValue(attribute_name='id',  top=1*cm ,left=0.5*cm),
            ObjectValue(attribute_name='placa',  top=1*cm, left=3*cm),
            )
		borders = {'all': False}

	class band_summary(ReportBand):
		height = 0.5*cm
		elements = [
            Label(text='Totals:',  top=1.5*cm),
            ObjectValue(expression='count(placa)',  top=1.5*cm, left=5*cm),
            ]
		borders = {'top': True}
		
	class band_page_footer(ReportBand):
		height = 0.5*cm
		elements = [
            Label(text='Geraldo Reports', top=0.1*cm),
            SystemField(expression='Printed in %(now:%Y, %b %d)s at %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
		borders = {'top': True}


