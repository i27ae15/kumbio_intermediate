from organization_info.utils.enums import FieldType

# TODO: implement more field types
# TODO: implement organization type field

# It is possible to create a third field that will be used to validate the information provided

DEFAULT_CLIENT_TYPES = [
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Medical patient',
        'description': 'A medical patient',
        'fields': [
            ('blood_type', FieldType.TEXT.value),
            ('initial_weight', FieldType.NUMBER.value),
            ('initial_height', FieldType.NUMBER.value),
            ('taking_medications', FieldType.TEXT.value),
            ('allergies', FieldType.TEXT.value),
            ('conditions_known', FieldType.TEXT.value),
            ('preferences', FieldType.TEXT.value)
        ]
    },
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Spa Client',
        'description': 'A spa client',
        'fields': [
            ('Has received professional', FieldType.TEXT.value),
            ('injuries or conditions', FieldType.TEXT.value),
            ('diseases', FieldType.TEXT.value),
            ('has received professional treatments on skin', FieldType.TEXT.value),
        ]
    },
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Pet',
        'description': 'A medical pet',
        'fields': [
            ('name', FieldType.TEXT.value),
            ('birth_date', FieldType.TEXT.value),
            ('age', FieldType.NUMBER.value),
            ('sterilized', FieldType.TEXT.value),
            ('weight', FieldType.NUMBER.value),
            ('active', FieldType.TEXT.value),
            ('species', FieldType.TEXT.value),
            ('race', FieldType.TEXT.value),
            ('gender', FieldType.TEXT.value),
            ('conditions_known', FieldType.TEXT.value),
            ('allergies', FieldType.TEXT.value),
            ('taking_medications', FieldType.TEXT.value),
            ('first_visit_reason', FieldType.TEXT.value),
            ('behavior', FieldType.TEXT.value),
        ]
    },
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Car',
        'description': 'A car',
        'fields': [
            ('brand', FieldType.TEXT.value),
            ('model', FieldType.TEXT.value),
            ('year', FieldType.NUMBER.value),
            ('license_plate', FieldType.TEXT.value),
            ('color', FieldType.TEXT.value),
        ]
    },
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Medical Patient',
        'description': 'A medical patient',
        'fields': [
            ('conditions_known', FieldType.TEXT.value),
            ('taking_medications', FieldType.TEXT.value),
            ('allergies', FieldType.TEXT.value),
            ('blood_type', FieldType.TEXT.value),
            ('initial_weight', FieldType.NUMBER.value),
            ('initial_height', FieldType.NUMBER.value),
            ('first_visit_reason', FieldType.TEXT.value),
            ('preferences', FieldType.TEXT.value)
        ]
    },
]
