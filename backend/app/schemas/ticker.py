from backend.app.schemas.__meta__ import Schema


class TickerSchema(Schema):
    name: str
    current_value: int


class TickerChangeSchema(Schema):
    ticker_id: int
    current_value: int