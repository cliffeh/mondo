# TODO

* more sensors
  * CPU
  * disk? (maybe not, or filtered by default)
* make it "production-ready"
  * tests (of any kind lol)
  * Hypercorn
* better logging
  * error cases
  * debugging/tracing
* signal handling (Quart doesn't like Ctrl-C with websocket clients attached)
* a `?help` message that helps inform what query params can be provided
* some kind of an admin status page
  * uptime
  * connected clients/queues
  * type/number of metrics collected
* instance-specific configs
* different display type for memory stats (line graph isn't the best)
