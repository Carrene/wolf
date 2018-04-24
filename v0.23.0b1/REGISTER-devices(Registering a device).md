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
    "createdAt":"2018-04-24T23:29:38.757303Z",
    "modifiedAt":null,
    "secret":"e5KLh2ZaaK96pC96\/np42pUPM5CXL1EaxqPJuKyRYlQ=\n",
    "phone":989122451075
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
    "createdAt":"2018-04-24T23:29:38.757303Z",
    "modifiedAt":"2018-04-24T23:29:38.880421Z",
    "secret":"DN5szKxa35cGCyg3DxAb+FqFl16IHraew5pCMUfDXas=\n",
    "phone":989122451075
}
```

