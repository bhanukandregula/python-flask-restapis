# Here we will be having our marshmallows schemas
from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # we will use this value while we are returning the data as response
    id = fields.Str(dump_only=True)
    item_name = fields.Str(required=True)
    item_price = fields.Float(required=True)
    # store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    # We don't need to validate both, we only need one
    item_name = fields.Str()
    item_price = fields.Float()
    store_id = fields.Int() # optional


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
