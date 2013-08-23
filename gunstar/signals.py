# -*- coding: utf-8 -*-
from blinker import signal


request_started_signal = signal('request-started-signal')
request_finished_signal = signal('request-finished-signal')
request_exception_signal = signal('request-exception-signal')
template_rendered_signal = signal('template-rendered-signal')
