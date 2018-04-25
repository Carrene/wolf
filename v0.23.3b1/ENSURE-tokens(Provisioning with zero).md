## Provisioning with zero

### ENSURE /apiv1/tokens

Trying to ensure token with provisioning with zero cryptomodule id

### Form

Name | Example
--- | ---
phone | 989122451075
name | DummyTokenName
cryptomoduleId | 0
expireDate | 1513434403

### Response: 400 Bad Request

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 66

#### Body

```json
{"message":"Bad Request","description":"Invalid cryptomodule id."}
```

