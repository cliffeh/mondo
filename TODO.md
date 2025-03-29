# TODO

* more sensors
  * CPU
  * memory
  * disk? (maybe not, or filtered by default)
* make it "production-ready"
  * tests (of any kind lol)
  * Hypercorn
* better logging
  * error cases
  * debugging/tracing
* signal handling (Quart doesn't like Ctrl-C with websocket clients attached)
* a `?help` message that helps inform what query params can be provided
* serve historical data
  * `?t` param for "how much data i want"
