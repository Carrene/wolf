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
    "createdAt":"2018-04-25T11:20:52.657013Z",
    "phone":989122451075,
    "secret":"iWBu8S4s2lq87OP5vX7hXXU8LggqyhlNoBc8Fv2vh4Q=\n",
    "modifiedAt":null
}
```

## WHEN: Trying to registering the same device again

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 187

#### Body

```json
{
    "createdAt":"2018-04-25T11:20:52.657013Z",
    "phone":989122451075,
    "secret":"v\/QYH2It37dEGjP2btdNVlwrWYXegX6hJltFD5COHoE=\n",
    "modifiedAt":"2018-04-25T11:20:52.781229Z"
}
```

