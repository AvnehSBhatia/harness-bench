# Payments client runbook

## Timeouts

Calls to the payments API time out after 10 seconds.

## Retries

When a call fails with a 5xx, the client retries. The first retry waits 1 second; each later retry waits twice as
long as the one before, but never more than 30 seconds. We never retry more than 6 times: if the caller asks for
more, it gets 6. Asking for a negative number of retries is a bug and raises ValueError.

## Alerts

Three failed calls in a row page the on-call engineer.
