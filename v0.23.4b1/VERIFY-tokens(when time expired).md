## when time expired

### VERIFY /apiv1/tokens/:token_id/codes/:code

Verifying time based OTP

### Url Parameters

Name | Example
--- | ---
token_id | 1
code | 97458A009AB01102

### Response: 461 Token is expired

#### Headers

* Content-Type: text/plain; charset=utf-8
* Content-Length: 48

#### Body

```
Token is expired
The requested token is expired.
```

