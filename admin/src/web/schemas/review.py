from marshmallow import Schema, fields, validate

# Endpoint crear review
class ReviewCreateSchema(Schema):
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=1000),
        error_messages={
            'required': 'This field is required',
            'invalid': 'Content cannot be empty'
        }
    )
    rating = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=5),
        error_messages={
            'required': 'This field is required',
            'invalid': 'Rating must be between 1 and 5'
        }
    )
    historic_site_id = fields.Int(
        required=True,
        error_messages={'required': 'This field is required'}
    )

# Endpoint actualizacion review
class ReviewUpdateSchema(Schema):
    content = fields.Str(
        allow_none=True,
        validate=validate.Length(min=1, max=1000),
        error_messages={'invalid': 'Content cannot be empty'}
    )
    rating = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=5),
        error_messages={
            'required': 'This field is required',
            'invalid': 'Rating must be between 1 and 5'
        }
    )

# Endpoint para obtener reviews
class ReviewSearchSchema(Schema):
    site = fields.Int(allow_none=True)
    page = fields.Int(
        missing=1,
        validate=validate.Range(min=1)
    )
    per_page = fields.Int(
        missing=25,
        validate=validate.Range(min=1, max=100)
    )