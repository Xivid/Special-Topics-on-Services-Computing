#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# soaplib - Copyright (C) 2009 Aaron Bickell, Jamie Kirkpatrick
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#

import soaplib

from soaplib.core.service import soap
from soaplib.core.service import DefinitionBase
from soaplib.core.model.primitive import String, Integer

from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
import sqlite3

class CourseGradeService(DefinitionBase):
    @soap(String, Integer, _returns=String)
    def getGrade(self, name, id):
        '''
        <b>getGrade</b>
        @param name the name of the course to query from
        @param id the student identification of whom to query for
        @return the score
        '''
        con = sqlite3.connect("Grade.db")
        cur = con.cursor()
        try:
            cur.execute("select "+ name + " from grade where id = " + str(id))
            result = str(id) + ' ' + name + ' ' + str(cur.fetchall()[0][0])
        except IndexError:
            result = "No such student."
        except sqlite3.OperationalError:
            result = "No such course."
        finally:
            return result


if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([CourseGradeService], 'tns')
        wsgi_application = wsgi.Application(soap_application)

        print "listening to http://0.0.0.0:23333"
        print "wsdl is at: http://localhost:23333/?wsdl"

        server = make_server('localhost', 23333, wsgi_application)
        server.serve_forever()

    except ImportError:
        print "Error: example server code requires Python >= 2.5"
