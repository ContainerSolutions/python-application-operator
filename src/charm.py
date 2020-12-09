#!/usr/bin/env python3
# Copyright 2020 kirek007@gmail.com <Marek Ruszczyk>
# See LICENSE file for licensing details.

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import MaintenanceStatus, ActiveStatus

logger = logging.getLogger(__name__)


class PythonApplicationOperatorCharm(CharmBase):
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_config_changed(self, _):
        if not self.unit.is_leader():
            logger.info('--------------- Im not a leader')
            self.unit.status = ActiveStatus()
            return

        self.unit.status = MaintenanceStatus('Setting pod spec.')

        logger.info('--------------- Building Pod Spec')
        config = self.model.config

        # vol_config_app = [
        #     {"name": "app-code", "mountPath": "/app", "emptyDir": {"medium": "Memory"}},
        #     {'name': 'app-helper-files', 'mountPath': '/data2', 'files': [{'path': 'start-app.sh', 'content': open("./files/start-app.sh").read()}]},
        #
        # ]
        vol_config = [
            # {"name": "git-secret", "mountPath": "/secrets", "secret": {"name": "charm-secrets"}},
            {"name": "app-code", "mountPath": "/app", "emptyDir": {"medium": "Memory"}},
            {'name': 'init-code-files', 'mountPath': '/data', 'files': [
                {'path': 'init-code.sh', 'content': open("./files/init-code.sh").read()},
                {'path': 'start-app.sh', 'content': open("./files/start-app.sh").read()}
            ]},
        ]

        spec = {
            'version': 3,
            'containers': [
                {
                    'name': self.app.name,
                    'imageDetails': {
                        'imagePath': config['image']
                    },
                    'args': ["bash", "/data/init-code.sh"],
                    'kubernetes': {},
                    "volumeConfig": vol_config,
                    'ports': [{
                        'containerPort': 3000,
                        'name': 'app-http',
                        'protocol': 'TCP',
                        }]
                },
                {
                    'init': True,
                    'name': self.app.name + "-code-init",
                    'imageDetails': {
                        'imagePath': config['image']
                    },
                    'args': ["bash", "/data/init-code.sh"],
                    'kubernetes': {},
                    "volumeConfig": vol_config,
                    'ports': [{
                        'containerPort': 3001,
                        'name': 'init-http',
                        'protocol': 'TCP'
                    }]
                },
            ],
            "kubernetesResources": {
                "services": [
                    {
                        "name": "my-service2",
                        "labels": {
                            "juju-app": self.app.name
                        },
                        "spec": {
                            "selector": {
                                "juju-app": self.app.name
                            },
                            "ports": [
                                {
                                    "protocol": "TCP",
                                    "port": 3000,
                                    "targetPort": 9376
                                }
                            ],
                            "type": "NodePort"
                        }
                    }
                ]
            },
        }
        logger.info('--------------- Run Pod Spec')
        logger.info(spec)

        self.model.pod.set_spec(spec)
        self.unit.status = ActiveStatus()

        return spec


if __name__ == "__main__":
    main(PythonApplicationOperatorCharm)
