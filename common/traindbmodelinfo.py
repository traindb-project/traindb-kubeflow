# Copyright 2023 The TrainDB-ML Authors.
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

import tdbconstants

class TDBModelInfo():
    """A manager for docker information for PyTorchJob client"""

    def __init__(self, 
                 registry, 
                 name_prefix, 
                 tag, 
                 modeltype):
        self.registry = registry
        self.image_name = name_prefix + modeltype
        self.tag = tag

    def full_image_name(self, tag):
        """Return the full image name
        
        :param tag: the new tag for the image

        """
        return '{}/{}:{}'.format(self.registry, self.image_name, tag)

    def pod_name(self, modeltype, modelname):
        """Return the full image name
        
        :param modeltype: the model type for TrainDB-ML
        :param modelname: the model name for TrainDB-ML

        """
        return '{}-{}-{}'.format(tdbconstants.TRAINDB_ML_TRAIN_PREFIX, modeltype, modelname)

    def pvc_name(self):
        """Return the persistent volume claim name
        """
        return tdbconstants.DEFAULT_PVC_NAME        

    def volume_name(self):
        """Return the persistent volume name
        """
        return tdbconstants.DEFAULT_VOLUME_NAME