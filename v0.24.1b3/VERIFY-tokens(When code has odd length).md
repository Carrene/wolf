## When code has odd length

### VERIFY /apiv1/tokens/:token_id/codes/:code

Verifying time based OTP

### Url Parameters

Name | Example
--- | ---
token_id | 1
code | badcode

### Response: 400 Invalid Code

#### Headers

* Content-Type: text/plain; charset=utf-8
* Content-Length: 52

#### Body

```
Bad Request
Bad request syntax or unsupported method
```

## WHEN: When code is malformed

### Response: 400 Invalid Code

#### Headers

* Content-Type: text/plain; charset=utf-8
* Content-Length: 52

#### Body

```
Bad Request
Bad request syntax or unsupported method
```

