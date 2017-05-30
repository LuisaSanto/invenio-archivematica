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

"""Test the factories."""

import tempfile
import uuid
from os.path import isdir, isfile, join
from shutil import rmtree

from invenio_files_rest.models import Bucket, Location
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_records_files.api import Record
from invenio_records_files.models import RecordsBuckets
from six import BytesIO

from invenio_archivematica import factories
from invenio_archivematica.models import Archive


def test_create_accessioned_id(db):
    """Test ``create_accessioned_id`` function."""
    # First, we create a record
    recid = uuid.uuid4()
    PersistentIdentifier.create(
        'recid',
        '42',
        object_type='rec',
        object_uuid=recid,
        status=PIDStatus.REGISTERED)
    Record.create({'title': 'record test'}, recid)
    accessioned_id = factories.create_accession_id('42', 'recid')
    assert accessioned_id == 'CERN-recid-42-0'


def test_transfer_cp(db):
    """Test factories.transfer_cp function."""
    # we setup a file storage
    tmppath = tempfile.mkdtemp()
    db.session.add(Location(name='default', uri=tmppath, default=True))
    db.session.commit()
    # first we create a record
    recid = uuid.uuid4()
    PersistentIdentifier.create(
        'recid',
        '1337',
        object_type='rec',
        object_uuid=recid,
        status=PIDStatus.REGISTERED)
    record = Record.create({'title': 'record test'}, recid)
    rec_dir = join(tmppath, factories.create_accession_id('1337', 'recid'))
    Archive.get_from_record(recid).accession_id = rec_dir
    # we add a file to the record
    bucket = Bucket.create()
    content = b'Aaah! A headcrab!!!\n'
    RecordsBuckets.create(record=record.model, bucket=bucket)
    record.files['crab.txt'] = BytesIO(content)
    # test!
    factories.transfer_cp(record.id, tmppath)
    assert isdir(rec_dir)
    assert isfile(join(rec_dir, 'crab.txt'))
    with open(join(rec_dir, 'crab.txt'), "rb") as f:
        assert f.read() == content
    # finalization
    rmtree(tmppath)


def test_transfer_rsync(db):
    """Test factories.transfer_rsync function."""
    # we setup a file storage
    tmppath = tempfile.mkdtemp()
    db.session.add(Location(name='default', uri=tmppath, default=True))
    db.session.commit()
    # first we create a record
    recid = uuid.uuid4()
    PersistentIdentifier.create(
        'recid',
        '42',
        object_type='rec',
        object_uuid=recid,
        status=PIDStatus.REGISTERED)
    record = Record.create({'title': 'lambda'}, recid)
    rec_dir = join(tmppath, factories.create_accession_id('42', 'recid'))
    Archive.get_from_record(recid).accession_id = rec_dir
    # we add a file to the record
    bucket = Bucket.create()
    content = b'Its on my head!!!\n'
    RecordsBuckets.create(record=record.model, bucket=bucket)
    record.files['zombie.txt'] = BytesIO(content)
    # test!
    config = {
        'destination': tmppath,
        'args': '-az'
    }
    factories.transfer_rsync(record.id, config)
    assert isdir(rec_dir)
    assert isfile(join(rec_dir, 'zombie.txt'))
    with open(join(rec_dir, 'zombie.txt'), "rb") as f:
        assert f.read() == content
    # finalization
    rmtree(tmppath)
