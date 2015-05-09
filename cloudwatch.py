import psutil
import os
from boto.ec2 import cloudwatch
from boto.utils import get_instance_metadata
import boto.ec2.autoscale

class Metric:
    _metrics = {}

    def add_metric(self, key, value, unit='Percent'):
        if unit not in self._metrics:
            self._metrics[unit] = {}

        self._metrics[unit].update({key: value})

    def _get_auto_scaling_group_name(self, instance_id, region):
        conn = boto.ec2.autoscale.AutoScaleConnection()
        boto.ec2.autoscale.connect_to_region(region)
        groups = conn.get_all_autoscaling_instances([instance_id])
        return groups[0].group_name if len(groups) > 0 else None

    def send(self):
        metadata = get_instance_metadata()
        instance_id = metadata['instance-id']
        region = metadata['placement']['availability-zone'][0:-1]

        cw = cloudwatch.connect_to_region(region)

        group = self._get_auto_scaling_group_name(instance_id, region)

        for (unit, metrics) in self._metrics.items():
            cw.put_metric_data('EC2', metrics.keys(), metrics.values(), unit=unit, dimensions={'InstanceId': instance_id})
            if group:
                cw.put_metric_data('EC2', metrics.keys(), metrics.values(), unit=unit, dimensions={'AutoScalingGroupName': group})

if __name__ == '__main__':

    cpu = psutil.cpu_percent(interval=20)
    mem = psutil.virtual_memory().percent

    m = Metric()
    m.add_metric('Real CPU Usage', cpu)
    m.add_metric('Memory Usage', mem)
    m.send()
