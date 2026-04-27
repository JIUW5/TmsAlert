from tms_alert_service.metrics import EVENT_FILTERED_TOTAL, EVENT_PROCESSED_TOTAL, EVENT_TOTAL
from tms_alert_service.models import N9eEvent
from tms_alert_service.services.aggregation_service import upsert_aggregation
from tms_alert_service.services.calendar_service import pass_trading_day_check
from tms_alert_service.services.owner_service import fetch_owner_mobile
from tms_alert_service.services.rule_service import fetch_rules, is_time_in_schedule
from tms_alert_service.services.time_utils import get_session_type, now_in_tz


async def process_event(event: N9eEvent) -> dict:
    status = event.status.lower()
    EVENT_TOTAL.labels(status=status).inc()

    ref_now = now_in_tz()
    session = get_session_type(ref_now)

    rules = fetch_rules(event.labels.hostname, event.labels.name)
    if not rules:
        EVENT_FILTERED_TOTAL.labels(reason='rule_not_found').inc()
        return {'accepted': False, 'reason': 'rule_not_found'}

    if not is_time_in_schedule(rules, ref_now):
        EVENT_FILTERED_TOTAL.labels(reason='out_of_schedule').inc()
        return {'accepted': False, 'reason': 'out_of_schedule'}

    if not await pass_trading_day_check(event.labels.ex, session, ref_now):
        EVENT_FILTERED_TOTAL.labels(reason='not_trading_day').inc()
        return {'accepted': False, 'reason': 'not_trading_day'}

    owner = rules[0].get('service_owner')
    mobile = fetch_owner_mobile(owner)

    upsert_aggregation(event, session, owner, mobile)
    EVENT_PROCESSED_TOTAL.inc()
    return {'accepted': True, 'aggregated': True}
