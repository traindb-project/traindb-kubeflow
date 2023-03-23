# Copyright 2022 The TrainDB-ML Authors.
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

DEFAULT_USER_AGENT = 'traindb-ml/{VERSION}'

# Job Constants
JOB_DEFAULT_NAME = 'traindb-ml-job-'
JOB_TYPE = 'pytorch'

# Serving Constants
SERVING_TYPE = 'kserve'

# persistent volume claim constants
PVC_DEFAULT_MOUNT_PATH = '/mnt'
DEFAULT_PVC_NAME = 'traindb-ml-pvc'
DEFAULT_VOLUME_NAME = 'traindb-ml-volume'

# TrainDB-ML Logging Constants
TRAINDB_ML_LOG_LEVEL = os.environ.get('TRAINDB_ML_LOG_LEVEL', 'INFO').upper()
TRAINDB_ML_LOG_FORMAT = '%(levelname)s|%(asctime)s|%(pathname)s|%(lineno)d| %(message)s'
TRAINDB_ML_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'

# TrainDB-ML namespace
DEFAULT_NAMESPACE = "default"
TRAINDB_ML_NAMESPACE = "traindb-ml"
TRAINDB_ML_TRAIN_PREFIX = "traindb-ml-train"