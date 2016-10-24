import rollbar
import sys
import json
from extra_utils import get_secrets
rollbar.init(get_secrets['rollbar_token'], 'production')
rollbar.report_message('System crash: ' + sys.argv[1], 'critical')
