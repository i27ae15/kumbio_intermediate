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
            ('allergies_sensitivities', FieldType.TEXT.value),
            ('injuries_surgeries', FieldType.TEXT.value),
            ('illnesses', FieldType.TEXT.value),
            ('professional_treatments', FieldType.TEXT.value),
            ('recent_major_surgery', FieldType.TEXT.value),
            ('list_injuries_surgeries', FieldType.TEXT.value),
            ('specific_concerns', FieldType.TEXT.value),
            ('skin_type', FieldType.TEXT.value),
            ('special_requests', FieldType.TEXT.value),
            ('visited_before', FieldType.TEXT.value),
            ('how_heard_about', FieldType.TEXT.value),
            ('confirmation_option', FieldType.TEXT.value)
        ]
    },
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Consultant',
        'description': 'Consultant',
        'fields': [
            ('business_name', FieldType.TEXT.value),
            ('industry', FieldType.TEXT.value),
            ('years_in_service', FieldType.NUMBER.value),
            ('strengths', FieldType.TEXT.value),
            ('weaknesses', FieldType.TEXT.value),
            ('unique_selling_proposition', FieldType.TEXT.value),
            ('how_heard_about', FieldType.TEXT.value),
            ('confirmation_option', FieldType.TEXT.value)
        ]
    },
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Real State',
        'description': 'Real State',
        'fields': [
            ('buyer_or_seller', FieldType.TEXT.value),
            ('property_type', FieldType.TEXT.value),
            ('geographic_area', FieldType.TEXT.value),
            ('price_range', FieldType.TEXT.value),
            ('specific_questions', FieldType.TEXT.value),
            ('worked_with_realtor_before', FieldType.TEXT.value),
            ('how_heard_about', FieldType.TEXT.value),
            ('confirmation_option', FieldType.TEXT.value)
        ]
    },
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Other',
        'description': 'Other',
        'fields': [
            ('', FieldType.TEXT.value),
        ]
    },
]
