# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Johann Prieur <johann.prieur@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from common import *

def transport_headers():
    """Returns a dictionary, containing transport (http) headers
    to use for the request"""

    return {}

def soap_action():
    """Returns the SOAPAction value to pass to the transport
    or None if no SOAPAction needs to be specified"""

    return "http://www.msn.com/webservices/AddressBook/FindMembership"

def soap_body(services_types, deltas_only, last_change):
    """Returns the SOAP xml body"""

    services = ''
    for service in services_types:
        services += """
                <ServiceType xmlns="http://www.msn.com/webservices/AddressBook">
                     %s
                </ServiceType>""" % service

    deltas = ''
    if deltas_only:
        deltas = """<View xmlns="http://www.msn.com/webservices/AddressBook">
                        Full
                    </View>
                    <deltasOnly xmlns="http://www.msn.com/webservices/AddressBook">
                        true
                    </deltasOnly>
                    <lastChange xmlns="http://www.msn.com/webservices/AddressBook">
                        %s
                    </lastChange>""" % last_change

    return """
       <FindMembership xmlns="http://www.msn.com/webservices/AddressBook">
           <serviceFilter xmlns="http://www.msn.com/webservices/AddressBook">
               <Types xmlns="http://www.msn.com/webservices/AddressBook">
                  %(services)s
               </Types>
           </serviceFilter>
           %(deltas)s
       </FindMembership>""" % { 'services' : services,
                                'deltas' : deltas }