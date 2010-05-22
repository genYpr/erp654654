#!/usr/bin/python

# -*- encoding: utf-8 -*-

#
# Copyright P. Christeas <p_christ@hol.gr> 2008
#
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###############################################################################

''' A script that will parse files from the cmd line and, if they
   are OpenERP modules, it will list their provides
'''

import sys
import os

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
(options, args) = parser.parse_args()


def get_module_info(tname):
	try:
		f = open(tname,"r")
		data = f.read()
		info = eval(data)
		#if 'version' in info:
		#	info['version'] = rel.version.rsplit('.', 1)[0] + '.' + info['version']+rel.subver
		f.close()
	except IOError:
		sys.stderr.write("Dir at %s may not be an OpenERP module.\n" % tname)
		return {}
	except:
		sys.stderr.write(str( sys.exc_info()))
		return {}
	return info

def get_ext_depends(deps):
	ret = []
	for dep in deps:
		if type(dep) == type(tuple()):
			ret.append(dep[0]+' '+ dep[1] + ' ' + dep[2])
		else:
			ret.append(dep)
	ret = set(ret)
	return ret

def get_depends(deps):
	ret = []
	for dep in deps:
		if dep == "base" : continue
		ret.append(dep)
	return set(ret)


openerp_reqs = []
openerp_provides = []
ext_reqs = []

for tfile in args:
        if os.path.basename(tfile) not in ('__terp__.py', '__openerp__.py'):
            continue
	info = get_module_info(tfile)
	if (info == {}):
		#no_dirs.append(bdir)
		pass
	else :
		openerp_provides.append(os.path.basename(os.path.dirname(tfile)))
		if 'depends' in info:
			openerp_reqs.extend(get_depends(info['depends']))
		if 'ext_depends' in info:
			ext_reqs.extend(get_ext_depends(info['ext_depends']))

# Check if this package provides all the modules it would depend upon:

req_fail = []
for dep in openerp_reqs:
	if dep not in openerp_provides:
		req_fail.append(dep)
		
if len(req_fail):
	sys.stderr.write("Included modules do not contain these required ones:\n%s\n" % 
		', '.join(req_fail))
	exit(1)

# Just print the external requires:
for d in ext_reqs:
	print d
