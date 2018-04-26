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
    "modifiedAt":null,
    "phone":989122451075,
    "secret":"moB0GiL0NIkCBdJXfySVzspcav4Dh1Sa+9a2PUD6duE=\n",
    "createdAt":"2018-04-26T15:21:48.123707Z"
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
    "modifiedAt":"2018-04-26T15:21:48.233213Z",
    "phone":989122451075,
    "secret":"NiZ\/aAmCSOzNrX1O9ZgrtZ5HDiIs0kPArnkOmCKrij8=\n",
    "createdAt":"2018-04-26T15:21:48.123707Z"
}
```

