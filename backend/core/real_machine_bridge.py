import random
import platform
import psutil

class RealMachineBridge:
    def __init__(self):
        pass

    def get_actual_metrics(self):
        try:
            cpu_load = psutil.cpu_percent(interval=0.1) / 100.0
            mem_pct = psutil.virtual_memory().percent / 100.0
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_info'])
                    processes.append({
                        'Id': pinfo['pid'],
                        'Name': pinfo['name'],
                        'CPU': pinfo['cpu_percent'] or 0,
                        'WorkingSet': pinfo['memory_info'].rss if pinfo['memory_info'] else 0
                    })
                except:
                    pass
            
            return {'real_cpu_load': cpu_load, 'real_mem_pct': mem_pct, 'processes': processes[:10]}
        except:
            return {'error': 'Unable to fetch metrics'}
