## Provisioning with empty token name

### ENSURE /apiv1/tokens

Provisioning with empty token name

### Form

Name | Example
--- | ---
phone | 989122451075
name | 
cryptomoduleId | 1
expireDate | 1513434403

### Response: 400 Bad Request

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Reason: insufficient-name-length
* Content-Length: 93

#### Body

```json
```

```{"message":"Bad Request","description":"Please enter at least 1 characters for field: name."}
```

