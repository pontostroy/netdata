# -*- coding: utf-8 -*-
# Description: journalbeat netdata python.d module
# Author: Andrusyak Iaroslav (pontostroy)

import json
from collections import defaultdict
from bases.FrameworkServices.UrlService import UrlService

# default module values (can be overridden per job in `config`)
update_every = 1
priority = 60000
retries = 60

ORDER = ['Main', 'Output','Pipeline', 'Traffic']

CHARTS = {
    'Main': {
        'options': [None, 'Libbeat events', 'Events', 'All events',
                    'Beats', 'area'],
        'lines': [
            ['acked_o', 'Acked in', 'incremental', 1, 1],
            ['acked_p', 'Acked out', 'incremental', 1, -1],
            ['total_o', 'Total in', 'incremental', 1, 1],
            ['total_p', 'Total out', 'incremental', 1, -1],
            ['failed_o', 'Failed', 'incremental', 1,1],
            ['published_p','Published', 'incremental',1,-1],
            #['active_o','Active', 'incremental',1,-1],
        ]
        },

    'Output': {
        'options': [None, 'Libbeat events', 'Events', 'All events',
                    'Beats', 'area'],
        'lines': [
            ["acked_o"],
            #["active_o"],
            ["batches_o"],
            ["dropped_o"],
            ["duplicates_o"],
            ["failed_o"],
            ["total_o"],
            ["read_errors"],
            ["write_errors"],
        ]
        },
    'Traffic': {
        'options': [None, 'Traffic', 'Kb', 'Traffic',
                    'Beats', 'area'],
        'lines': [
             ['read_bytes', 'read', 'incremental', 1, 1 << 10],
             ['write_bytes', 'write', 'incremental', 1, -1 << 10]
        ]
        },
    'Pipeline': {
        'options': [None, 'Pipeline events', 'Events', 'All events',
                    'Beats', 'area'],
        'lines': [
            ["acked_p"],
            #["active_p"],
            ["dropped_p"],
            ["failed_p"],
            ["filtered_p"],
            ["published_p"],
            ["retry_p"],
            ["total_p"],
        ]
        }
}


class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.url = self.configuration.get('url', 'http://127.0.0.1:5066/stats')
        self.order = ORDER
        self.definitions = CHARTS

    def _get_data(self):
        raw_data = self._get_raw_data()
        if not raw_data:
            return None

        data = json.loads(raw_data)

        output_j = data['libbeat']['output']['events']
        traffic_r = data['libbeat']['output']['read']
        traffic_w = data['libbeat']['output']['write']
        pipeline_j = data['libbeat']['pipeline']['events']
        queue_j = data['libbeat']['pipeline']['queue']
        return {
            'acked_o': output_j['acked'],
            'active_o': output_j['active'],
            'batches_o': output_j['batches'],
            'dropped_o': output_j['dropped'],
            'duplicates_o': output_j['duplicates'],
            'failed_o': output_j['failed'],
            'total_o': output_j['total'],
            'read_errors': traffic_r['errors'],
            'write_errors': traffic_w['errors'],
            'read_bytes': traffic_r['bytes'],
            'write_bytes': traffic_w['bytes'],
            'acked_p': queue_j['acked'],
            'active_p': pipeline_j['active'],
            'dropped_p': pipeline_j['dropped'],
            'failed_p': pipeline_j['failed'],
            'filtered_p': pipeline_j['filtered'],
            'published_p': pipeline_j['published'],
            'retry_p': pipeline_j['retry'],
            'total_p': pipeline_j['total']
            }
