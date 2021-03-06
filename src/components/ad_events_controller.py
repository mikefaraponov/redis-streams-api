from redis import Redis


class AdEventsController:
    def __init__(self, conn: Redis):
        self.conn = conn

    def process_ad_event(self, event: dict):
        if 'type' in event:
            print(event)
            self.conn.xadd(event["type"], event, '*')
