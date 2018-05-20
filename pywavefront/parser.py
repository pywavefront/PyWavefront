# ----------------------------------------------------------------------------
# PyWavefront
# Copyright (c) 2013 Kurt Yoder
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of PyWavefront nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os
import logging

class Parser(object):
    """This defines a generalized parse dispatcher; all parse functions
    reside in subclasses."""
    strict = False

    def read_file(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                self.parse(line, dir=os.path.dirname(file_name))

    def parse(self, line, dir):
        """Determine what type of line we are and dispatch
        appropriately."""
        if line.startswith('#'):
            return

        values = line.split()
        if len(values) < 2:
            return

        line_type = values[0]
        args = values[1:]
        i = 0
        for arg in args:
            if dir != '' and ('mtllib' in line or 'map_Kd' in line):
                args[i] = dir + '/' + arg
            else:
                args[i] = arg
            i += 1

        attrib = 'parse_%s' % line_type

        if Parser.strict:
            parse_function = getattr(self, attrib)
            parse_function(args)
        elif hasattr(self, attrib):
            parse_function = getattr(self, attrib)
            parse_function(args)
        else:
            logging.warning("Unimplemented OBJ format statement '%s' on line '%s'"
                            % (line_type, line.rstrip()))
