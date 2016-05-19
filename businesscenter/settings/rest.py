
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    #'DEFAULT_PAGINATION_CLASS': 'backends.paginators.CustomPagination',
    'PAGE_SIZE': 12,
    'ORDERING_PARAM': 'o',
    #'DATE_INPUT_FORMATS': ['iso-8601', '%d.%m.%Y'],
    'DEFAULT_PERMISSION_CLASSES': (
        'utils.permissions.IsAdminOrReadOnly',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    )
}