## Registering a device

### REGISTER /apiv1/devices

Registering a device by phone and_ udid

### Form

Name | Example
--- | ---
phone | 989122451075
udid | 2b6f0cc904d137be2e1730235f5664094b831186

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 161

#### Body

```json
{
    "phone":989122451075,
    "createdAt":"2018-05-01T19:31:32.610829Z",
    "secret":"kFLu2GYs5vmBlbtBEBI2K2iSB5MYR8JdWLXD9LUhYZE=\n",
    "modifiedAt":null
}
```

## WHEN: Trying to registering the same device again

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 186

#### Body

```json
{
    "phone":989122451075,
    "createdAt":"2018-05-01T19:31:32.610829Z",
    "secret":"XwbFTTPIkhpkRPNgCpByUNEUd+jBWnChyLqmXcP7TtE=\n",
    "modifiedAt":"2018-05-01T19:31:32.729163Z"
}
```

