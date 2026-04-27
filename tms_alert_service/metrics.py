from prometheus_client import Counter, Gauge, Histogram

EVENT_TOTAL = Counter('tms_event_total', 'Total n9e events received', ['status'])
EVENT_FILTERED_TOTAL = Counter('tms_event_filtered_total', 'Events filtered by reason', ['reason'])
EVENT_PROCESSED_TOTAL = Counter('tms_event_processed_total', 'Events accepted and aggregated')
WEBHOOK_SEND_TOTAL = Counter('tms_webhook_send_total', 'Webhook send attempts', ['result'])
EVENT_LATENCY = Histogram('tms_event_latency_seconds', 'End-to-end event handling latency')
PENDING_AGGREGATION = Gauge('tms_pending_aggregation_records', 'Pending aggregation records not flushed')
