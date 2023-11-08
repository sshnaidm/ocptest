from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

import logging


class Logger:
    def __init__(self, module=None):
        if module:
            self.log = AnsibleLog(module)
        else:
            logging.basicConfig(level=logging.DEBUG)
            self.log = logging


class AnsibleLog:
    def __init__(self, module):
        self.module = module

    def debug(self, msg):
        self.module.log(msg, log_args={"priority": "7"})

    def info(self, msg):
        self.module.log(msg, log_args={"priority": "6"})

    def warning(self, msg):
        self.module.log(msg, log_args={"priority": "4"})

    def error(self, msg):
        self.module.log(msg, log_args={"priority": "3"})

    def critical(self, msg):
        self.module.log(msg, log_args={"priority": "2"})

    def exception(self, msg):
        self.module.log(msg, log_args={"priority": "1"})


def get_url(url, module=None, fail_on_error=True):
    log = Logger(module).log
    if module and getattr(module, "params", None) and module.params.get("validate_certs") is not None:
        verify = module.params.get("validate_certs", True)
    else:
        verify = True
    log.info(f"Getting {url}")
    response = requests.get(url=url, verify=verify, timeout=120)
    log.debug(f"Got {url} status_code:{response.status_code}")
    # "priority": "7"})
    if not response.ok:
        if fail_on_error:
            raise Exception(
                f"Failed to get {url}: status_code: {response.status_code} content: {response.content}")
        return None
    return response.text
