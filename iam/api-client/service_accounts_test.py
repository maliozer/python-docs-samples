# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from googleapiclient.errors import HttpError

import service_accounts


def test_service_accounts(capsys):
    project_id = os.environ['GCLOUD_PROJECT']
    name = 'python-test-{}'.format(str(uuid.uuid4()).split('-')[0])
    email = name + '@' + project_id + '.iam.gserviceaccount.com'

    try:
        service_accounts.create_service_account(
            project_id, name, 'Py Test Account')
        service_accounts.list_service_accounts(project_id)
        service_accounts.rename_service_account(
            email, 'Updated Py Test Account')
        service_accounts.disable_service_account(email)
        service_accounts.enable_service_account(email)
        service_accounts.delete_service_account(email)
    finally:
        try:
            service_accounts.delete_service_account(email)
        except HttpError as e:
            # When the service account doesn't exist, the service returns 403.
            if '403' in str(e):
                print("Ignoring 403 error upon cleanup.")
            else:
                raise
