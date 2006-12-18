# -*- coding: utf-8 -*-
#
# Copyright (C) 2005  Ole André Vadla Ravnås <oleavr@gmail.com>
# Copyright (C) 2006  Ali Sabil <ali.sabil@gmail.com>
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

"""Incomming data parsers."""

from gnet.constants import *

import gobject

__all__ = ['AbstractParser', 'DelimiterParser']

class AbstractParser(gobject.GObject):
    """Base class for all stateful parsers.
    
        @since: 0.1"""
    __gsignals__ = {
            "received": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (gobject.TYPE_STRING,))
            }
    def __init__(self, transport):
        """Initializer
        
            @param transport: the transport used to receive data
            @type transport: an object derived from
                L{network.AbstractClient}"""
        gobject.GObject.__init__(self)
        transport.connect("received", self._on_received)
        transport.connect("notify::status", self._on_status_change)
        self._transport = transport
        self._reset_state()

    def _reset_state(self):
        """Needs to be overriden in order to implement the default
        parser state."""
        raise NotImplementedError

    def _on_status_change(self, transport, param):
        raise NotImplementedError

    def _on_received(self, transport, buf, length):
        raise NotImplementedError


class DelimiterParser(AbstractParser):
    """Receiver class that emit received signal when a chunk of data is
    received.
    
    A chunk is defined by a delimiter which is either a string or an integer.

    @since: 0.1"""

    def __init__(self, transport):
        """Initializer
        
            @param transport: the transport used to receive data
            @type transport: L{network.AbstractClient}"""
        AbstractParser.__init__(self, transport)
        self._chunk_delimiter = "\n"
        
    def _reset_state(self):
        self._recv_cache = ""

    def _on_status_change(self, transport, param):
        status = transport.get_property("status")
        if status == STATUS_OPEN:
            self.__init_state()

    def _on_received(self, transport, buf, length):
        self._recv_cache += buf
        if self._process_recv_cache():
            gobject.idle_add(self._process_recv_cache, priority=gobject.PRIORITY_LOW) 

    def _process_recv_cache(self):
        if len(self._recv_cache) == 0:
            return False
        if self._chunk_delimiter is None or self._chunk_delimiter == "":
            self.emit("received", self._recv_cache)
            self._recv_cache = ""
        elif isinstance(self._chunk_delimiter, int):
            available = len(self._recv_cache)
            required = self._chunk_delimiter
            if required <= available:
                self.emit ("received", self._recv_cache[:required])
                self._recv_cache = self._recv_cache[required:]
        else:
            s = self._recv_cache.split(self._chunk_delimiter,1)
            if len(s) > 1:
                self.emit ("received", s[0])
                self._recv_cache = s[1]
            else:
                self._recv_cache = s[0]
        
        if len(self._recv_cache) == 0:
            return False
        return True

    def _set_chunk_delimiter(self, delimiter):
        self._chunk_delimiter = delimiter
    def _get_chunk_delimiter(self):
        return self._chunk_delimiter
    delimiter = property(_get_chunk_delimiter,
        _set_chunk_delimiter,
        doc="""The chunk delimiter, can be either a string or
        an integer that specify the number of bytes for each chunk""")
gobject.type_register(DelimiterParser)
