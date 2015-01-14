# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2015 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Santiago Dueñas <sduenas@bitergia.com>
#

import argparse

from sortinghat import api
from sortinghat.command import Command
from sortinghat.exceptions import NotFoundError


class Move(Command):
    """Move an identity into a unique identity.

    This command moves <from_id> identity into <to_uuid> unique identity.
    When <to_uuid> is the unique identity that is currently related to
    <from_id>, the command does not have any effect.
    """
    def __init__(self, **kwargs):
        super(Move, self).__init__(**kwargs)

        self._set_database(**kwargs)

        self.parser = argparse.ArgumentParser(description=self.description,
                                              usage=self.usage)

        # Positional arguments
        self.parser.add_argument('from_id',
                                 help="Identity to move")
        self.parser.add_argument('to_uuid',
                                 help="Move into this unique identity")

    @property
    def description(self):
        return """Move an identity into a unique identity."""

    @property
    def usage(self):
        return "%(prog)s mv <from_id> <to_uuid>"

    def run(self, *args):
        """Move an identity into a unique identity.

        When <from_id> or <to_uuid> are empty the command does not have any
        effect. The same happens when both <from_id> is currently related to
        <to_uuid>.
        """
        params = self.parser.parse_args(args)

        from_id = params.from_id
        to_uuid = params.to_uuid

        self.move(from_id, to_uuid)

    def move(self, from_id, to_uuid):
        """Move an identity into a unique identity.

        The method moves the identity identified by <from_id> to
        the unique identity <to_uuid>.

        When <to_uuid> is the unique identity that is currently related to
        <from_id>, the action does not have any effect. The same occurs when
        either <from_id> or <to_uuid> are None or empty.

        :param from_id: identifier of the identity set to be moved
        :param to_uuid: identifier of the unique identity where 'from_id'
            will be moved
        """
        if not from_id or not to_uuid:
            return

        try:
            api.move_identity(self.db, from_id, to_uuid)
            self.display('move.tmpl',
                         from_id=from_id, to_uuid=to_uuid)
        except NotFoundError, e:
            self.error(str(e))