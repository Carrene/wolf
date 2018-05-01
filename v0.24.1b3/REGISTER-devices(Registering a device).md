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
* Content-Length: 162

#### Body

```json
{
    "phone":989122451075,
    "secret":"C5\/02aBlXwk5g7WmHyp9+7ZCixFqvQOfwSmuvnME720=\n",
    "modifiedAt":null,
    "createdAt":"2018-05-01T19:34:20.032485Z"
}
```

## WHEN: Trying to registering the same device again

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 188

#### Body

```json
{
    "phone":989122451075,
    "secret":"Whm\/LgfPKSO2NvzXfYoxg7OIRCuVJnqPKpegDT\/IzKs=\n",
    "modifiedAt":"2018-05-01T19:34:20.143209Z",
    "createdAt":"2018-05-01T19:34:20.032485Z"
}
```

