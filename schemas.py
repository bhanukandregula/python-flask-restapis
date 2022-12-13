# Here we will be having our marshmallows schemas
from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # we will use this value while we are returning the data as response
    id = fields.Int(dump_only=True)
    item_name = fields.Str(required=True)
    item_price = fields.Float(required=True)
    # store_id = fields.Str(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    # We don't need to validate both, we only need one
    item_name = fields.Str()
    item_price = fields.Float()
    store_id = fields.Int()  # optional


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # load_only=True
    password = fields.Str(required=True)
