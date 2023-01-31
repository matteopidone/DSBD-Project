import ast

class MetricCalculator :
    ## Variable of the class
    metrics = {}
    interval_time_list = list()
    numberOfViolations = []

    ''' PAST VIOLATION FUNCTIONS '''
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
                            if value < int(stat['threshold']):
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


    ''' FUTURE VIOLATION FUNCTIONS '''
    def get_number_future_violation(self, sla, all_metrics):
        result = list()
        dict_sla = ast.literal_eval(sla)
        for metric in dict_sla['sla_metrics'] :
            metric_set = {}
            metric_set['metric_name'] = metric['metric_name']
            metric_set['stats'] = self.get_stats_with_future_violations(metric['stats'], metric['metric_name'], all_metrics)
            result.append(metric_set)
        return { "sla_metrics": result }


    def get_stats_with_future_violations(self, stats, metric_name, all_metrics):
        result = list()
        for stat in stats :
            stat.update({'violations': []})
            stats_new = self.get_violation_from_future(stat, metric_name, all_metrics)
            result.append(stats_new)
        return result

    def get_violation_from_future(self, stat, metric_name, all_metrics) :
        list_metrics = ast.literal_eval(all_metrics)
        for metric in list_metrics :
            if( metric['name'] == metric_name ) :
                if( stat['name'] == 'MAX' ) :
                    violation = 0
                    for value in metric['values'][0]['value']:
                        if float(value) > int(stat['threshold']):
                            violation += 1
                    stat['violations'].append({'10min': violation})

                elif( stat['name'] == 'MIN' ) :
                    violation = 0
                    for value in metric['values'][1]['value']:
                        if float(value) < int(stat['threshold']):
                            violation += 1
                    stat['violations'].append({'10min': violation})

        return stat


    