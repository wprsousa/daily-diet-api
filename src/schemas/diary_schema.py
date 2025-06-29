from flask_marshmallow import Marshmallow
from marshmallow import fields

from src.models.diary import Diary

ma = Marshmallow()


class DiarySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Diary
        load_instance = True

    id = ma.auto_field()
    name = fields.String(required=True)
    description = ma.auto_field()
    date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    in_diet = fields.Boolean(required=False)

