from elasticapm.conf.constants import ERROR
from elasticapm.processors import for_events

@for_events(ERROR)
def my_processor(client, event):
    if 'exception' in event and 'stacktrace' in event['exception']:
        event['exception'].pop('stacktrace')
    return event