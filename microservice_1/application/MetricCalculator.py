import ast

class MetricCalculator :
    ## Variable of the class
    metrics = {}
    interval_time_list = list()
    numberOfViolations = []
    numberViolationsPrototype = {
    "sla_metrics" : [
        {
            "metric_name": "cpu",
            "stats": [
                {
                    "name": "MAX",
                    "threshold": 50
                },
                {
                    "name": "MIN",
                    "threshold": 20
                }
            ]
        },
        {
            "metric_name": "disk",
            "stats": [
                {
                    "name": "MAX",
                    "threshold": 80,
                    "violations": [
                        {
                            "time" :"1h",
                            "value": 22
                        },
                        {
                            "time" :"3h",
                            "value": 22
                        },
                    ]
                },
                {
                    "name": "MIN",
                    "threshold": 35
                }
            ]
        }
    ]
}

    def get_violation_from_all_hour(self, stat, metric_name, all_metrics) :
        dict_all_metrics = ast.literal_eval(all_metrics)
        for interval_time in ['1h', '3h', '12h'] :
            list_metrics = dict_all_metrics[interval_time]
            for metric in list_metrics :
                if( metric['__name__'] == metric_name ) :
                    if( stat['name'] == 'MAX' ) :
                        violation = 0
                        for value in metric['values']:
                            if value > int(stat['threshold']):
                                violation += 1
                        stat['violations'].append({interval_time: violation})

                    elif( stat['name'] == 'MIN' ) :
                        violation = 0
                        for value in metric['values']:
                            if value > int(stat['threshold']):
                                violation += 1
                        stat['violations'].append({interval_time: violation})

        return stat

    def get_stats_with_violations(self, stats, metric_name, all_metrics):
        result = list()
        for stat in stats :
            stat.update({'violations': []})
            stats_new = self.get_violation_from_all_hour(stat, metric_name, all_metrics)
            result.append(stats_new)
        return result

    def get_number_violation(self, sla, all_metrics) :
        result = list()
        dict_sla = ast.literal_eval(sla)
        for metric in dict_sla['sla_metrics'] :
            metric_set = {}
            metric_set['metric_name'] = metric['metric_name']
            metric_set['stats'] = self.get_stats_with_violations(metric['stats'], metric['metric_name'], all_metrics)
            result.append(metric_set)
        return { "sla_metrics": result }


            


    