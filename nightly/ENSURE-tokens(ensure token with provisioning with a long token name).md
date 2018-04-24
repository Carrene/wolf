## ensure token with provisioning with a long token name

### ENSURE /apiv1/tokens

Trying to ensure token with provisioning with a long token name

### Form

Name | Example
--- | ---
phone | 989122451075
name | MoreThan50Charsxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
cryptomoduleId | 1
expireDate | 1513434403

### Response: 400 Bad Request

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Reason: extra-name-length
* Content-Length: 84

#### Body

```json
{"message":"Bad Request","description":"Cannot enter more than: 50 in field: name."}
```

