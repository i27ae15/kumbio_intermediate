from organization_info.utils.enums import FieldType

# It is possible to create a third field that will be used to validate the information provided

DEFAULT_CLIENT_TYPES = [
    {
        'organization' : int(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Patient',
        'description': 'A medical patient',
        'fields': [
            ('gender', FieldType.TEXT.value),
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
    {
        'organization' : int(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Pet',
        'description': 'A medical pet',
        'fields': [
            ('species', FieldType.TEXT.value),
            ('race', FieldType.TEXT.value),
            ('initial_weight', FieldType.NUMBER.value),
            ('gender', FieldType.TEXT.value),
            ('conditions_known', FieldType.TEXT.value),
            ('allergies', FieldType.TEXT.value),
            ('taking_medications', FieldType.TEXT.value),
            ('first_visit_reason', FieldType.TEXT.value),
            ('behavior', FieldType.TEXT.value),
           
        ]
    },
]
