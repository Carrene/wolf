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
* Content-Length: 163

#### Body

```json
{
    "createdAt":"2018-04-26T15:19:21.287399Z",
    "secret":"fTm2nQ\/iNAzK7Fsdsm\/YHBjXgCsft3OrzSrgvFWGn9k=\n",
    "phone":989122451075,
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
    "createdAt":"2018-04-26T15:19:21.287399Z",
    "secret":"Oz\/R15awbEMPRioHuP1AzltDUfsvxNK7mJsp7FUHp40=\n",
    "phone":989122451075,
    "modifiedAt":"2018-04-26T15:19:21.422081Z"
}
```

