from marshmallow import Schema, fields


class PlainStoreSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.String(required=True)


class PlainItemSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.String(required=True)
  price = fields.Float(required=True)
  description = fields.String()


class PlainTagSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str()


class StoreSchema(PlainStoreSchema):
  items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
  tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class ItemSchema(PlainItemSchema):
  store_id = fields.Int(required=True, load_only=True)
  store = fields.Nested(PlainStoreSchema(), dump_only=True)
  tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
  store_id = fields.Int(load_only=True)
  store = fields.Nested(PlainStoreSchema(), dump_only=True)
  items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagItemSchema(Schema):
  message = fields.Str()
  item = fields.Nested(ItemSchema)
  tag = fields.Nested(TagSchema)


class StoreUpdateSchema(Schema):
  name = fields.String(required=True)


class ItemUpdateSchema(Schema):
  name = fields.String()
  price = fields.Float()
  store_id = fields.Int()


class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True)
  password = fields.Str(required=True, load_only=True)
