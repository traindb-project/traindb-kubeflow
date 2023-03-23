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

import logging

from unicodedata import name
from venv import create
import yaml
from os import path
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException

LOG = logging.getLogger(__name__)

### Input parameters
CONF_PATH = '/opt/traindb/traindb-ml/conf/' # This is client side directory (Kubernetes/Kubeflow Python Client)
HOST_PATH = '/opt/traindb/traindb-ml/models' # This is host side directory
NAMESPACE = 'learned-model'
SYSTEM_NAME = 'traindb'
TDB_NAME = 'traindb-ml'

### Constants for template yaml files
PV_TEMPLATE = 'template-pv.yaml'
PVC_TEMPLATE = 'template-pvc.yaml'
VOL_POSTFIX = '-volume'
CLAIM_POSTFIX = '-claim'
PV_POSTFIX = '-pv.yaml'
PVC_POSTFIX = '-pvc.yaml'

class TrainDBMLInitializer():
    def __init__(self, tdbnamespace=None) -> None:
        self.namespace = tdbnamespace

    def open_yaml(self, filename):
        with open(filename) as f:
            pv_config = yaml.load(f, Loader=yaml.FullLoader)
        return pv_config

    def write_pv_yaml(self, filename, pv_config, name=TDB_NAME, system=SYSTEM_NAME, hostpath=HOST_PATH):
        pv_config['metadata']['name'] = name + VOL_POSTFIX
        pv_config['metadata']['labels']['system'] = system
        pv_config['metadata']['labels']['name'] = name + VOL_POSTFIX
        pv_config['spec']['hostPath']['path'] = hostpath

        with open(filename, 'w') as f:
            yaml.dump(pv_config, f)

    def write_pvc_yaml(self, filename, pv_config, name=TDB_NAME, system=SYSTEM_NAME, hostpath=HOST_PATH):
        pv_config['metadata']['name'] = name + CLAIM_POSTFIX
        pv_config['metadata']['namespace'] = name
        pv_config['spec']['selector']['matchLabels']['system'] = system
        pv_config['spec']['selector']['matchLabels']['name'] = name + VOL_POSTFIX

        with open(filename, 'w') as f:
            yaml.dump(pv_config, f)

    ### Create YAML files
    def create_pv_yaml_from_template(self, conf_path, namespace, system=SYSTEM_NAME, hostpath=HOST_PATH):
        pv_conf = self.open_yaml(conf_path+ PV_TEMPLATE)
        yaml_filename = conf_path + namespace + PV_POSTFIX
        self.write_pv_yaml(yaml_filename, pv_conf, namespace, system, hostpath)

    def create_pvc_yaml_from_template(self, conf_path, namespace, system=TDB_NAME, hostpath=HOST_PATH):
        pv_conf = self.open_yaml(conf_path+ PVC_TEMPLATE)
        yaml_filename = conf_path + namespace + PVC_POSTFIX
        self.write_pvc_yaml(yaml_filename, pv_conf, namespace, system, hostpath)

    ### Deploy PV, PVC using YAML files
    def deploy_yaml(self, yaml_file, namespace=HOST_PATH):
        config.load_kube_config()
        k8s_client = client.ApiClient()
        return utils.create_from_yaml(k8s_client,yaml_file,verbose=True)

    def get_pv_filename(self, conf_path, namespace):
        return conf_path + namespace + PV_POSTFIX
    def get_pvc_filename(self, conf_path, namespace):
        return conf_path + namespace + PVC_POSTFIX

    def create_namespace(self, namespace=None):
        config.load_kube_config()
        if namespace:
            v1 = client.CoreV1Api()
            try:
                v1.read_namespace(name=namespace)
            except ApiException:
                body = client.V1Namespace(
                    kind="Namespace",
                    api_version="v1", 
                    metadata=client.V1ObjectMeta(name=namespace)
                )
                try:
                    v1.create_namespace(body=body)
                except ApiException as e:
                    LOG.error(
                        "Exception when calling CoreV1Api->read_namespace: %s",
                        e,
                    )

    def delete_namespace(self, namespace=None):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        try:
            v1.read_namespace(name=namespace)
        except ApiException as e:
            LOG.error(
                "Requested {namespace} does not exist. %s",
                e,
            )

        v1.delete_namespace(namespace)


    def init(self, tdb_namespace=NAMESPACE):
        self.create_pv_yaml_from_template(CONF_PATH, tdb_namespace, system=SYSTEM_NAME, hostpath=HOST_PATH)
        self.create_pvc_yaml_from_template(CONF_PATH, tdb_namespace, system=SYSTEM_NAME, hostpath=HOST_PATH)

        if self.deploy_yaml(self.get_pv_filename(CONF_PATH, namespace=tdb_namespace)):
            print("Persistent volume is successfully created.")
        else:
            raise Exception("The requested persistent volume already existed.")

        if self.deploy_yaml(self.get_pvc_filename(CONF_PATH, namespace=tdb_namespace)):
            print("Persistent volume claim is successfully created.")
        else:
            raise Exception("The requested persistent volume claim already existed.")

##################################################################################################################
if __name__ == "__main__":
    tdb_ml_initializer = TrainDBMLInitializer('sungsoo')
    # tdb_ml_initializer.create_namespace(namespace='sungsoo')
    # tdb_ml_initializer.init('sungsoo')
    tdb_ml_initializer.delete_namespace('sungsoo')
