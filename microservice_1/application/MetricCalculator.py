
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

    def get_violation_from_all_hour(stat, metric_name) :
        for interval_time in self.interval_time_list :
            list_metrics = self.metrics[interval_time]
            for metric in list_metrics :
                if( metric['__name__'] == metric_name ) :
                    if( stat['name'] == 'MAX' ) :
                        ## calcolo max ad ogni ora
                        violation = 2
                        stat['violations'].add(interval_time, violation)

                    elif( stat['name'] == 'MIN' ) :
                        ## calcolo min ad ogni ora
                        violation = 2
                        stat['violations'].add(interval_time, violation)

        return stat_to_find

    def get_stats_with_violations(self, stats, metric_name):
        result = list()
        for stat in stats :
            stat.append('violations', list())
            stats_new = self.get_violation_from_all_hour(stat, metric_name)
            result.append(stats_new)
        return result

    def get_number_violation(self, sla) :
        result = list()
        for metric in sla['sla_metrics'] :
            metric_set = {}
            metric_set['metric_name'] = metric['metric_name']
            metric_set['stats'] = self.get_stats_with_violations(metric['stats'], metric['metric_name'])
            result.append(metric_set)
        return { "sla_metrics": result }


            


    