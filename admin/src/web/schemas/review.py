from marshmallow import Schema, fields, validate

# Schema crear review
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

# Schema actualizacion review
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

# Schema para obtener reviews con filtros (GET /api/reviews)
class ReviewSearchSchema(Schema):
    site = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
        error_messages={'invalid': 'Site ID must be a positive integer'}
    )
    page = fields.Int(
        load_default=1,
        validate=validate.Range(min=1),
        error_messages={'invalid': 'Page must be greater than 0'}
    )
    per_page = fields.Int(
        load_default=25,
        validate=validate.Range(min=1, max=100),
        error_messages={'invalid': 'per_page must be between 1 and 100'}
    )

# Schema para obtener reviews de un usuario (GET /api/reviews/users/<user_id>/reviews)
class UserReviewsSearchSchema(Schema):
    page = fields.Int(
        load_default=1,
        validate=validate.Range(min=1),
        error_messages={'invalid': 'Page must be greater than 0'}
    )
    per_page = fields.Int(
        load_default=25,
        validate=validate.Range(min=1, max=100),
        error_messages={'invalid': 'per_page must be between 1 and 100'}
    )