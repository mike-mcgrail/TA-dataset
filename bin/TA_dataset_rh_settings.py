
import import_declare_test

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    MultipleModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunktaucclib.rest_handler.admin_external import AdminExternalHandler
import logging

util.remove_http_proxy_env_vars()


fields_dataset_parameters = [
    field.RestField(
        'dataset_environment',
        required=True,
        encrypted=False,
        default='us',
        validator=None
    ), 
    field.RestField(
        'dataset_log_read_access_key',
        required=False,
        encrypted=True,
        default='',
        validator=validator.String(
            max_len=100, 
            min_len=0, 
        )
    ), 
    field.RestField(
        'dataset_log_write_access_key',
        required=False,
        encrypted=True,
        default='',
        validator=validator.String(
            max_len=100, 
            min_len=0, 
        )
    )
]
model_dataset_parameters = RestModel(fields_dataset_parameters, name='dataset_parameters')


fields_logging = [
    field.RestField(
        'loglevel',
        required=False,
        encrypted=False,
        default='INFO',
        validator=None
    )
]
model_logging = RestModel(fields_logging, name='logging')


fields_proxy = [
    field.RestField(
        'proxy_enabled',
        required=False,
        encrypted=False,
        default=None,
        validator=None
    ), 
    field.RestField(
        'proxy_url',
        required=False,
        encrypted=False,
        default=None,
        validator=validator.String(
            max_len=4096, 
            min_len=0, 
        )
    ), 
    field.RestField(
        'proxy_port',
        required=False,
        encrypted=False,
        default=None,
        validator=validator.Number(
            max_val=65535, 
            min_val=1, 
        )
    ), 
    field.RestField(
        'proxy_username',
        required=False,
        encrypted=False,
        default=None,
        validator=validator.String(
            max_len=50, 
            min_len=0, 
        )
    ), 
    field.RestField(
        'proxy_password',
        required=False,
        encrypted=True,
        default=None,
        validator=validator.String(
            max_len=8192, 
            min_len=0, 
        )
    )
]
model_proxy = RestModel(fields_proxy, name='proxy')


endpoint = MultipleModel(
    'ta_dataset_settings',
    models=[
        model_dataset_parameters, 
        model_logging, 
        model_proxy
    ],
)


if __name__ == '__main__':
    logging.getLogger().addHandler(logging.NullHandler())
    admin_external.handle(
        endpoint,
        handler=AdminExternalHandler,
    )
