# -*- coding: utf-8 -*-
###############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones <www.trey.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
###############################################################################

{
    'name': 'Checkout Require VAT',
    'category': 'website',
    'summary': 'Fuerza la introducción del NIF/CIF en el proceso de compra de '
               'la tienda online.',
    'version': '8.0.0.1',
    'description': '''
    Además de la mencionada validación, incluye ayudas para introducir el campo
    NIF o CIF en el checkout y autocompleta con el código del país en caso de
    no haberse indicado (actualmente solo España).
    ''',
    'author': 'Trey (www.trey.es)',
    'depends': [
        'website_attributes',
        'website_sale',
    ],
    'data': [
        'views/website_sale_require_vat.xml',
        'views/website_sale.xml'
    ],
    'installable': True,
}
