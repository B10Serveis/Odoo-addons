# -*- coding: utf-8 -*-
{
    'name': "Informe de tancament de caixa TPV",
    'summary': """Informe de tancament de caixa TPV""",   
    'author': "Batista10",
    'website': "https://www.batista10.cat",
    'category': 'Reports',
    'version': '10.0.0.0.4',
    'depends': ['base','report','point_of_sale'],
    'license': 'AGPL-3', 
    'application': True,
    'data': [
			'wizard/pos_wizard_report.xml',
        	'views/pos_closing.xml',
        	'views/pos_closing_report.xml'
			],
}

