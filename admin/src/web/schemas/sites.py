from marshmallow import Schema, fields, validate, post_load

# Schema para recibir parametros en endpoint de get sitios
class HistoricSiteSearchSchema(Schema):
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    province = fields.Str(allow_none=True)
    tags = fields.Str(allow_none=True)
    order_by = fields.Str(
        load_default='latest',
        validate=validate.OneOf(['latest', 'oldest', 'rating-5-1', 'rating-1-5'])
    )
    lat = fields.Float(
        allow_none=True,
        validate=validate.Range(-90, 90)
    )
    long = fields.Float(
        allow_none=True,
        validate=validate.Range(-180, 180)
    )
    radius = fields.Float(
        allow_none=True,
        validate=validate.Range(0.1, 1000)
    )
    page = fields.Int(
        load_default=1,
        validate=validate.Range(min=1)
    )
    per_page = fields.Int(
        load_default=20,
        validate=validate.Range(min=1, max=100)
    )

# Schema para recibir parametros en endpoint de crear sitio
class HistoricSiteCreateSchema(Schema):
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'This field is required'}
    )
    short_description = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={'required': 'This field is required'}
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'This field is required'}
    )
    city = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={'required': 'This field is required'}
    )
    province = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={'required': 'This field is required'}
    )
    lat = fields.Float(
        required=True,
        validate=validate.Range(-90, 90),
        error_messages={
            'required': 'This field is required',
            'invalid': 'Must be a number'
        }
    )
    long = fields.Float(
        required=True,
        validate=validate.Range(-180, 180),
        error_messages={
            'required': 'This field is required',
            'invalid': 'Must be a number'
        }
    )
    state_of_conservation = fields.Str(
        required=True,
        validate=validate.OneOf(['excelente', 'bueno', 'regular', 'malo']),
        error_messages={'required': 'This field is required'}
    )
    tags = fields.List(fields.Str(), load_default=[], allow_none=True)
    country = fields.Str(load_default='AR', validate=validate.Length(max=3))