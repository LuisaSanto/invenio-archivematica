# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""API for Invenio 3 module to connect Invenio to Archivematica."""

from invenio_archivematica.tasks import oais_fail_transfer, \
    oais_finish_transfer, oais_process_transfer, oais_start_transfer


def start_transfer(record, accession_id=''):
    """Start the archive process for a record.

    Start the transfer of the record in asynchronous mode. See
    :py:mod:`invenio_archivematica.tasks`
    :param record: the record to archive
    :type record: :py:class:`invenio_records.api.Record`
    :param str accession_id: the accessioned ID in archivematica. You can
    compute it from
    :py:func:`invenio_archivematica.factories.create_accession_id`
    """
    oais_start_transfer.delay(str(record.id), accession_id)


def process_transfer(record, aip_id=None):
    """Create the archive for a record.

    Process the transfer of the record in asynchronous mode. See
    :py:mod:`invenio_archivematica.tasks`
    :param record: the record to archive
    :type record: :py:class:`invenio_records.api.Record`
    :param str aip_id: the ID of the AIP in Archivematica
    """
    oais_process_transfer.delay(str(record.id), aip_id)


def process_aip(record, aip_id=None):
    """Create the archive for a record.

    Process the aip of the record in asynchronous mode. See
    :py:mod:`invenio_archivematica.tasks`
    :param record: the record to archive
    :type record: :py:class:`invenio_records.api.Record`
    :param str aip_id: the ID of the AIP in Archivematica
    """
    oais_process_aip.delay(str(record.id), aip_id)


def finish_transfer(record, aip_id):
    """Finish the archive process for a record.

    Finish the transfer of the record in asynchronous mode. See
    :py:mod:`invenio_archivematica.tasks`
    :param record: the record to archive
    :type record: :py:class:`invenio_records.api.Record`
    :param str aip_id: the ID of the created AIP in Archivematica
    """
    oais_finish_transfer.delay(str(record.id), aip_id)


def fail_transfer(record):
    """Fail the archive process for a record.

    Fail the transfer of the record in asynchronous mode. See
    :py:mod:`invenio_archivematica.tasks`
    :param record: the record to archive
    :type record: :py:class:`invenio_records.api.Record`
    """
    oais_fail_transfer.delay(str(record.id))
