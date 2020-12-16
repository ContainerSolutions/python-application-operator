#!/usr/bin/env python3
# Copyright 2020 kirek007@gmail.com <Marek Ruszczyk>
# See LICENSE file for licensing details.

import logging

import ops.lib
from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import MaintenanceStatus, ActiveStatus, BlockedStatus

logger = logging.getLogger(__name__)
pgsql = ops.lib.use("pgsql", 1, "postgresql-charmers@lists.launchpad.net")

DATABASE_NAME = "appdb"


class PythonApplicationOperatorCharm(CharmBase):
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.db = pgsql.PostgreSQLClient(self, 'db')  # 'db' relation in metadata.yaml
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.db.on.database_relation_joined, self._on_database_relation_joined)
        self.framework.observe(self.db.on.master_changed, self._master_changed)

        self._stored.db_conn_str = ""
        self._stored.database_enabled = False
        self._stored.database_ready = False
        self._stored.database_name = ""
        self._stored.database_name_updated = False

    def _on_database_relation_joined(self, event: pgsql.DatabaseRelationJoinedEvent):
        if self.model.unit.is_leader():
            config = self.model.config
            event.database = config["database_name"]
            logger.info("Requested database! {}".format(event.database))
        elif event.database != DATABASE_NAME:
                event.defer()
                return

    def _master_changed(self, event: pgsql.MasterChangedEvent):
        if event.database != DATABASE_NAME:
            return

        self._stored.db_conn_str = None if event.master is None else event.master.conn_str
        logger.info("Got database info! {}".format(self._stored.db_conn_str))
        self._stored.database_ready = True
        self._update_pod()

    def _update_pod(self):
        self.unit.status = MaintenanceStatus('Updating configuration...')

        config = self.model.config
        env_config = {}

        if not config["git_repo"]:
            self.unit.status = BlockedStatus('Git repository is not provided')
            return

        if self._stored.database_ready:
            logger.info("Injecting database data")
            env_config = {
                "DATABASE_{}_CON_STR".format(config["database_name"]) : self._stored.db_conn_str
            }

        vol_config = [
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
                    'args': ["bash", "/data/init-code.sh", config['git_repo'],config['entrypoint'], config['gunicorn_workers'], config['application_port']],
                    'kubernetes': {},
                    "volumeConfig": vol_config,
                    "envConfig": env_config,
                    'ports': [{
                        'containerPort': int(config['application_port']),
                        'name': 'app-http',
                        'protocol': 'TCP',
                    }]
                },
            ],
        }
        logger.info(spec)

        self.model.pod.set_spec(spec)
        self.unit.status = ActiveStatus()

    def _on_config_changed(self, _):
        if not self.unit.is_leader():
            self.unit.status = ActiveStatus()
            return

        self._update_pod()


if __name__ == "__main__":
    main(PythonApplicationOperatorCharm)
