## Provisioning with an expired token

### ENSURE /apiv1/tokens

Provisioning with an expired token

### Form

Name | Example
--- | ---
phone | 989122451075
name | ExpiredToken
cryptomoduleId | 1
expireDate | 1513434403

### Response: 461 Token is expired

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 78

#### Body

```json
{"message":"Token is expired","description":"The requested token is expired."}
```

