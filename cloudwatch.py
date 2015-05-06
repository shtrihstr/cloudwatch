import psutil
from boto.ec2 import cloudwatch
from boto.utils import get_instance_metadata

class Metric:
    _metrics = {}

    def add_metric(self, key, value, unit='Percent'):
        if unit not in self._metrics:
            self._metrics[unit] = {}

        self._metrics[unit].update({key: value})

    def send(self):
        metadata = get_instance_metadata()
        instance_id = metadata['instance-id']
        region = metadata['placement']['availability-zone'][0:-1]

        cw = cloudwatch.connect_to_region(region)

        for (unit, metrics) in self._metrics.items():
            cw.put_metric_data('EC2', metrics.keys(), metrics.values(), unit=unit, dimensions={"InstanceId": instance_id})
            print

if __name__ == '__main__':

    cpu = psutil.cpu_percent(interval=20)
    mem = psutil.virtual_memory().percent

    m = Metric()
    m.add_metric('Real CPU Usage', cpu)
    m.add_metric('Memory Usage', mem)
    m.send()
