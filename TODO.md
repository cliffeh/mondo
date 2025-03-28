# TODO

* make it simpler to add new metrics, with both http and websocket routes
  * more sensors
    * CPU
    * memory
    * disk? (maybe not, or filtered by default)
* hover details
* websocket disconnect/reconnect/error handling
* make it "production-ready" (UWSGI, gunicorn, etc.)
* tests (of any kind lol)
* server-side caching of the last N data points
* better chart legends
  * figure out z-axis for rollover highlighting (bring to front)
* signal handling (`Ctrl-C` breakage)
* better logging
  * error cases
  * debugging/tracing
* signal handling (Quart doesn't like Ctrl-C with clients attached)
* a `?help` message that helps inform what query params can be provided
