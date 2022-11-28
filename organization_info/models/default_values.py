from organization_info.utils.enums import FieldType

DEFAULT_CLIENT_TYPES = [{
    'organization' : int(), # id of the organization or the Organization object itself
    'name': 'pet',
    'description': 'This is a pet',
    'fields': [('race', FieldType.TEXT.value), ('number_of_vaccines', FieldType.NUMBER.value)]
}]