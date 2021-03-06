# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from urlparse import urljoin
import os

# 3rd party
import mock
import json

from tests.checks.common import AgentCheckTest, Fixtures

# IDs
CLUSTER_NAME = 'SparkCluster'

# Resource manager URI
RM_ADDRESS = 'http://localhost:8088'

# Service URLs
YARN_CLUSTER_METRICS_URL = urljoin(RM_ADDRESS, '/ws/v1/cluster/metrics')
YARN_APPS_URL = urljoin(RM_ADDRESS, '/ws/v1/cluster/apps') + '?states=RUNNING'
YARN_NODES_URL = urljoin(RM_ADDRESS, '/ws/v1/cluster/nodes')
YARN_SCHEDULER_URL = urljoin(RM_ADDRESS, '/ws/v1/cluster/scheduler')

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'ci')

collected_from_app_url = False

def requests_get_mock(*args, **kwargs):

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return json.loads(self.json_data)

        def raise_for_status(self):
            return True

    if args[0] == YARN_CLUSTER_METRICS_URL:
        with open(Fixtures.file('cluster_metrics', sdk_dir=FIXTURE_DIR), 'r') as f:
            body = f.read()
            return MockResponse(body, 200)

    elif args[0] == YARN_APPS_URL:
        with open(Fixtures.file('apps_metrics', sdk_dir=FIXTURE_DIR), 'r') as f:
            body = f.read()
            global collected_from_app_url
            collected_from_app_url = True
            return MockResponse(body, 200)

    elif args[0] == YARN_NODES_URL:
        with open(Fixtures.file('nodes_metrics', sdk_dir=FIXTURE_DIR), 'r') as f:
            body = f.read()
            return MockResponse(body, 200)

    elif args[0] == YARN_SCHEDULER_URL:
        with open(Fixtures.file('scheduler_metrics', sdk_dir=FIXTURE_DIR), 'r') as f:
            body = f.read()
            return MockResponse(body, 200)


class YARNCheck(AgentCheckTest):

    CHECK_NAME = 'yarn'

    YARN_CONFIG = {
        'resourcemanager_uri': 'http://localhost:8088',
        'cluster_name': CLUSTER_NAME,
        'tags': [
            'opt_key:opt_value'
        ],
        'application_tags': {
            'app_id': 'id',
            'app_queue': 'queue'
        },
        'queue_blacklist': [
            'nofollowqueue'
        ]
    }

    YARN_CONFIG_EXCLUDING_APP = {
        'resourcemanager_uri': 'http://localhost:8088',
        'cluster_name': CLUSTER_NAME,
        'tags': [
            'opt_key:opt_value'
        ],
        'application_tags': {
            'app_id': 'id',
            'app_queue': 'queue'
        },
        'collect_app_metrics': 'false'
    }

    YARN_CLUSTER_METRICS_VALUES = {
        'yarn.metrics.apps_submitted': 0,
        'yarn.metrics.apps_completed': 0,
        'yarn.metrics.apps_pending': 0,
        'yarn.metrics.apps_running': 0,
        'yarn.metrics.apps_failed': 0,
        'yarn.metrics.apps_killed': 0,
        'yarn.metrics.reserved_mb': 0,
        'yarn.metrics.available_mb': 17408,
        'yarn.metrics.allocated_mb': 0,
        'yarn.metrics.total_mb': 17408,
        'yarn.metrics.reserved_virtual_cores': 0,
        'yarn.metrics.available_virtual_cores': 7,
        'yarn.metrics.allocated_virtual_cores': 1,
        'yarn.metrics.total_virtual_cores': 8,
        'yarn.metrics.containers_allocated': 0,
        'yarn.metrics.containers_reserved': 0,
        'yarn.metrics.containers_pending': 0,
        'yarn.metrics.total_nodes': 1,
        'yarn.metrics.active_nodes': 1,
        'yarn.metrics.lost_nodes': 0,
        'yarn.metrics.unhealthy_nodes': 0,
        'yarn.metrics.decommissioned_nodes': 0,
        'yarn.metrics.rebooted_nodes': 0,
    }

    YARN_CLUSTER_METRICS_TAGS = [
        'cluster_name:%s' % CLUSTER_NAME,
        'opt_key:opt_value'
    ]

    YARN_APP_METRICS_VALUES = {
        'yarn.apps.progress': 100,
        'yarn.apps.started_time': 1326815573334,
        'yarn.apps.finished_time': 1326815598530,
        'yarn.apps.elapsed_time': 25196,
        'yarn.apps.allocated_mb': 0,
        'yarn.apps.allocated_vcores': 0,
        'yarn.apps.running_containers': 0,
        'yarn.apps.memory_seconds': 151730,
        'yarn.apps.vcore_seconds': 103,
    }

    YARN_APP_METRICS_TAGS = [
        'cluster_name:%s' % CLUSTER_NAME,
        'app_name:word count',
        'app_queue:default',
        'opt_key:opt_value'
    ]

    YARN_NODE_METRICS_VALUES = {
        'yarn.node.last_health_update': 1324056895432,
        'yarn.node.used_memory_mb': 0,
        'yarn.node.avail_memory_mb': 8192,
        'yarn.node.used_virtual_cores': 0,
        'yarn.node.available_virtual_cores': 8,
        'yarn.node.num_containers': 0,
    }

    YARN_NODE_METRICS_TAGS = [
        'cluster_name:%s' % CLUSTER_NAME,
        'node_id:h2:1235',
        'opt_key:opt_value'
    ]

    YARN_ROOT_QUEUE_METRICS_VALUES = {
        'yarn.queue.root.max_capacity': 100,
        'yarn.queue.root.used_capacity': 35.012,
        'yarn.queue.root.capacity': 100
    }

    YARN_ROOT_QUEUE_METRICS_TAGS = [
        'cluster_name:%s' % CLUSTER_NAME,
        'queue_name:root',
        'opt_key:opt_value'
    ]

    YARN_QUEUE_METRICS_VALUES = {
        'yarn.queue.num_pending_applications': 0,
        'yarn.queue.user_am_resource_limit.memory': 2587968,
        'yarn.queue.user_am_resource_limit.vcores': 688,
        'yarn.queue.absolute_capacity': 52.12,
        'yarn.queue.user_limit_factor': 1,
        'yarn.queue.user_limit': 100,
        'yarn.queue.num_applications': 3,
        'yarn.queue.used_am_resource.memory': 2688,
        'yarn.queue.used_am_resource.vcores': 3,
        'yarn.queue.absolute_used_capacity': 31.868685,
        'yarn.queue.resources_used.memory': 3164800,
        'yarn.queue.resources_used.vcores': 579,
        'yarn.queue.am_resource_limit.vcores': 688,
        'yarn.queue.am_resource_limit.memory': 2587968,
        'yarn.queue.capacity': 52.12,
        'yarn.queue.num_active_applications': 3,
        'yarn.queue.absolute_max_capacity': 52.12,
        'yarn.queue.used_capacity': 61.14484,
        'yarn.queue.num_containers': 75,
        'yarn.queue.max_capacity': 52.12,
        'yarn.queue.max_applications': 5212,
        'yarn.queue.max_applications_per_user': 5212
    }

    YARN_QUEUE_METRICS_TAGS = [
        'cluster_name:%s' % CLUSTER_NAME,
        'queue_name:clientqueue',
        'opt_key:opt_value'
    ]

    YARN_QUEUE_NOFOLLOW_METRICS_TAGS = [
        'cluster_name:%s' % CLUSTER_NAME,
        'queue_name:nofollowqueue',
        'opt_key:opt_value'
    ]

    def setUp(self):
        global collected_from_app_url
        collected_from_app_url = False

    @mock.patch('requests.get', side_effect=requests_get_mock)
    def test_check_excludes_app_metrics(self, mock_requests):
        config = {
            'instances': [self.YARN_CONFIG_EXCLUDING_APP]
        }

        self.run_check(config)

        # Check that the YARN App metrics is empty
        self.assertFalse(collected_from_app_url)

    @mock.patch('requests.get', side_effect=requests_get_mock)
    def test_check(self, mock_requests):
        config = {
            'instances': [self.YARN_CONFIG]
        }

        self.run_check(config)

        # Check the YARN Cluster Metrics
        for metric, value in self.YARN_CLUSTER_METRICS_VALUES.iteritems():
            self.assertMetric(metric,
                value=value,
                tags=self.YARN_CLUSTER_METRICS_TAGS)

        # Check the YARN App Metrics
        for metric, value in self.YARN_APP_METRICS_VALUES.iteritems():
            self.assertMetric(metric,
                value=value,
                tags=self.YARN_APP_METRICS_TAGS)

        # Check the YARN Node Metrics
        for metric, value in self.YARN_NODE_METRICS_VALUES.iteritems():
            self.assertMetric(metric,
                value=value,
                tags=self.YARN_NODE_METRICS_TAGS)

        # Check the YARN Root Queue Metrics
        for metric, value in self.YARN_ROOT_QUEUE_METRICS_VALUES.iteritems():
            self.assertMetric(metric,
                value=value,
                tags=self.YARN_ROOT_QUEUE_METRICS_TAGS)

        # Check the YARN Custom Queue Metrics
        for metric, value in self.YARN_QUEUE_METRICS_VALUES.iteritems():
            self.assertMetric(metric,
                value=value,
                tags=self.YARN_QUEUE_METRICS_TAGS)

        # Check the YARN Queue Metrics from excluded queues are absent
        self.assertMetric('yarn.queue.absolute_capacity', count=0, tags=self.YARN_QUEUE_NOFOLLOW_METRICS_TAGS)
