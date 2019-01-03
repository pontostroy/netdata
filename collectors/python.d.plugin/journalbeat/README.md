# journalbeat

Module uses the `monitoring` API to provide statistics.


```yaml
update_every : 1
priority     : 60000

local:
  url     : 'http://localhost:5066/stats'
```

Without configuration, module attempts to connect to `http://localhost:5066/stats`.

---
