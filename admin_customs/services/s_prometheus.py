import json
from prometheus_api_client import PrometheusConnect, PrometheusApiClientException
from django.http import JsonResponse

class prometheus():
    def __init__(self):
        self.prom = PrometheusConnect(url="http://prometheus.dockeronline.ovh:80", disable_ssl=True)

    def get_metrics_cpu(self):
        try:
            query = 'rate(node_cpu_seconds_total{mode!="idle"}[5m])'
            cpu_usage_data = self.prom.custom_query(query=query)

            # Calculer le pourcentage d'utilisation CPU
            cpu_usage = sum([float(result['value'][1]) for result in cpu_usage_data]) * 100
            cpu_usage= round(cpu_usage,2)
            # Retourner les données encodées en JSON
            return JsonResponse({'cpu_usage': cpu_usage})
        except PrometheusApiClientException as e:
            return JsonResponse({'error': str(e)})
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)})




    def get_metrics_ram(self):
        try:
            # Requêtes pour la mémoire totale et disponible
            query_total = 'node_memory_MemTotal_bytes'
            query_avail = 'node_memory_MemAvailable_bytes'

            total_data = self.prom.custom_query(query=query_total)
            avail_data = self.prom.custom_query(query=query_avail)

            # Assurer que les données sont alignées et calculer le pourcentage
            for total, avail in zip(total_data, avail_data):
                if total['metric']['instance'] == avail['metric']['instance']:
                    total_mem = float(total['value'][1])
                    available_mem = float(avail['value'][1])
                    used_mem_percent = 100 * (1 - (available_mem / total_mem))
                    return JsonResponse({'ram_usage': round(used_mem_percent, 2)})

            return JsonResponse({'error': 'RAM data not aligned'})
        except PrometheusApiClientException as e:
            return JsonResponse({'error': str(e)})
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)})

    def get_metrics_disk(self):
        try:
            # Requêtes pour la taille totale et l'espace disponible du disque
            query_size = 'sum(node_filesystem_size_bytes{fstype!~"tmpfs|overlay"})'
            query_avail = 'sum(node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"})'

            size_data = self.prom.custom_query(query=query_size)
            avail_data = self.prom.custom_query(query=query_avail)

            # Vérifier et calculer le pourcentage
            if size_data and avail_data:
                total_size = float(size_data[0]['value'][1])
                available_size = float(avail_data[0]['value'][1])
                used_disk_percent = 100 * (1 - (available_size / total_size))
                return JsonResponse({'disk_usage': round(used_disk_percent, 2)})

            return JsonResponse({'error': 'Disk data not available'})
        except PrometheusApiClientException as e:
            return JsonResponse({'error': str(e)})
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)})