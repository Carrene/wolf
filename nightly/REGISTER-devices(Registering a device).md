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
```

```{
    "phone":989122451075,
    "createdAt":"2018-04-24T22:34:13.133241Z",
    "modifiedAt":null,
    "secret":"BmMJbQrAo\/WdysmRy3PN8jpqByvGeRlVBXBHbpvNE1c=\n"
}
```

## WHEN: Trying to registering the same device again

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 187

#### Body

```json
```

```{
    "phone":989122451075,
    "createdAt":"2018-04-24T22:34:13.133241Z",
    "modifiedAt":"2018-04-24T22:34:13.248997Z",
    "secret":"ObpjdW097ZVhaB2KjeC2wD+FXOBMtlCx3E5ElrCr\/54=\n"
}
```

