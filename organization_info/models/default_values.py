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
        ],
        'spanish_fields': [
            ('tipo de sangre', FieldType.TEXT.value),
            ('peso inicial', FieldType.NUMBER.value),
            ('altura inicial', FieldType.NUMBER.value),
            ('tomando medicamentos', FieldType.TEXT.value),
            ('alergias', FieldType.TEXT.value),
            ('condiciones conocidas', FieldType.TEXT.value),
            ('preferencias', FieldType.TEXT.value)
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
        ],
        'spanish_fields': [
            ('alergias o sensibilidades', FieldType.TEXT.value),
            ('lesiones cirugías', FieldType.TEXT.value),
            ('enfermedades', FieldType.TEXT.value),
            ('tratamientos profesionales', FieldType.TEXT.value),
            ('cirugía importante reciente', FieldType.TEXT.value),
            ('lista lesiones cirugías', FieldType.TEXT.value),
            ('preocupaciones especificas', FieldType.TEXT.value),
            ('tipo de piel', FieldType.TEXT.value),
            ('solicitudes especiales', FieldType.TEXT.value),
            ('visitado anteriormente', FieldType.TEXT.value),
            ('como se entero', FieldType.TEXT.value),
            ('opción de confirmación', FieldType.TEXT.value)
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
        ],
        'spanish_fields': [
            ('nombre del negocio', FieldType.TEXT.value),
            ('industria', FieldType.TEXT.value),
            ('años de servicio', FieldType.NUMBER.value),
            ('fortalezas', FieldType.TEXT.value),
            ('debilidades', FieldType.TEXT.value),
            ('propuesta única de venta', FieldType.TEXT.value),
            ('cómo se enteró', FieldType.TEXT.value),
            ('opción de confirmación', FieldType.TEXT.value)
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
        ],
        'spanish_fields': [
            ('comprador o vendedor', FieldType.TEXT.value),
            ('tipo de propiedad', FieldType.TEXT.value),
            ('área geográfica', FieldType.TEXT.value),
            ('rango de precios', FieldType.TEXT.value),
            ('preguntas específicas', FieldType.TEXT.value),
            ('trabajado con un corredor antes', FieldType.TEXT.value),
            ('cómo se enteró', FieldType.TEXT.value),
            ('opción de confirmación', FieldType.TEXT.value)
        ]
    },
    {
        'organization' : str(), # id of the organization or the Organization object itself, depends on how it is created
        'name': 'Other',
        'description': 'Other',
        'fields': [
            ('', FieldType.TEXT.value),
        ],
        'spanish_fields': [
            ('', FieldType.TEXT.value),
        ]
    },
]
