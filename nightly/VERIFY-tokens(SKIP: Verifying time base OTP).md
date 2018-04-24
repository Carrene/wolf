## SKIP: Verifying time base OTP

### VERIFY /apiv1/tokens/:token_id/codes/:code

Test on another time

### Url Parameters

Name | Example
--- | ---
token_id | 1
code | 8E45779CD9825818

### Response: 200 OK

## WHEN: Trying to verify an invalid code

### Url Parameters

Name | Example
--- | ---
code | A44D8403A381641D
token_id | 1

### Response: 400 Invalid Code

#### Headers

* Content-Type: text/plain; charset=utf-8
* Content-Length: 52

#### Body

```
```

```Bad Request
Bad request syntax or unsupported method
```

