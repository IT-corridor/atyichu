
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    #'DEFAULT_PAGINATION_CLASS': 'backends.paginators.CustomPagination',
    'PAGE_SIZE': 10,
    'ORDERING_PARAM': 'o',
    #'DATE_INPUT_FORMATS': ['iso-8601', '%d.%m.%Y'],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
