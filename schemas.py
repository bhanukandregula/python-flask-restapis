# Here we will be having our marshmallows schemas
from marshmallow import Schema, fields


class ItemSchema(Schema):
    # we will use this value while we are returning the data as response
    id = fields.Str(dump_only=True)
    item_name = fields.Str(required=True)
    item_price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    # We don't need to validate both, we only need one
    item_name = fields.Str()
    item_price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
