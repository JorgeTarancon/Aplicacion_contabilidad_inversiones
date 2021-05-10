### BACKEND
pipenv install djangorestframwork django-cors-headers

Add these two modules to the installed_apps variable on backend/settings.py, and corsheaders.middleware.CorsMiddleware to the middleware variable in such file.

To the bottom of the same file
CORS_ORIGIN_WHITELIST = [
     'http://localhost:3000'
]

This will be the frontend webapp, which will need to be allowed to access this backend app.

A serializers.py must be created at the self_index_app directory in order to convert to JSON the relational database values. Also, there will be created some views that will return values depending on the queries.