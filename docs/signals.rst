Signals
============

Gunstar signal support is provided by the excellent `Blinker <http://pythonhosted.org/blinker/>`_ library.

=========================
request_started_signal
=========================

This signal is sent when request started.

Example:

.. code-block:: python

    from gunstar.signals import request_started_signal

    def receive_request_started_signal(app, request):
        print(app)
        print(request)

    request_started_signal.connect(receive_request_started_signal)

=========================
request_finished_signal
=========================

This signal is sent when response is sent to the client.

Example:

.. code-block:: python

    from gunstar.signals import request_finished_signal

    def receive_request_finished_signal(app, response):
        print(app)
        print(response)

    request_finished_signal.connect(receive_request_finished_signal)

=========================
request_exception_signal
=========================

This signal is sent when an exception happens during request processing.

Example:

.. code-block:: python

    from gunstar.signals import request_exception_signal

    def receive_request_exception_signal(app, request, exc_info):
        print(app)
        print(request)
        print(exc_info)

    request_exception_signal.connect(receive_request_exception_signal)

=========================
template_rendered_signal
=========================

This signal is sent when a template was successfully rendered.

Example:

.. code-block:: python

    from gunstar.signals import template_rendered_signal

    def receive_template_rendered_signal(app, handler, template, context):
        print(app)
        print(handler)
        print(template)
        print(context)

    template_rendered_signal.connect(receive_template_rendered_signal)
