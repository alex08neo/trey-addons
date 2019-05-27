# -*- coding: utf-8 -*-
###############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2016-Today Trey, Kilobytes de Soluciones <www.trey.es>
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'Sale discount',
    'category': 'Sales',
    'summary': 'Add discount to sale orders.',
    'version': '8.0.0.1',
    'description': '''
Wizard to add a discount in sale order lines considering only the products
that have marked the field 'Apply sale discount' in its template.''',
    'author': 'Trey (www.trey.es)',
    'depends': [
        'product',
        'sale',
    ],
    'data': [
        'security/security.xml',
        'wizards/sale_discount.xml',
        'views/product_template.xml',
    ],
    'installable': True,
}
