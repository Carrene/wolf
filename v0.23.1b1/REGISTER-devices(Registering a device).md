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
    "createdAt":"2018-04-25T09:02:19.341574Z",
    "modifiedAt":null,
    "phone":989122451075,
    "secret":"wJ54OKScqYCtMe0KLPhuSYI4UxJ0pjf55H65THJfqZ8=\n"
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
    "createdAt":"2018-04-25T09:02:19.341574Z",
    "modifiedAt":"2018-04-25T09:02:19.521899Z",
    "phone":989122451075,
    "secret":"EIA1kxebECEGkygUWrhz+EZ3QzseC9dZ1Vy\/To6f6x8=\n"
}
```

