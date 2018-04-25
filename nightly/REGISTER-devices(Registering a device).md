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
    "secret":"BydLH+WHs4zXrtg2svBU3JuAvqjFH7TLq6sJGve8ftA=\n",
    "phone":989122451075,
    "createdAt":"2018-04-25T12:00:24.331993Z"
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
    "modifiedAt":"2018-04-25T12:00:24.472532Z",
    "secret":"DRD0EH2ThL+xe8aIgVfBn4WDvL\/yAWVpc2RJSmIkDiE=\n",
    "phone":989122451075,
    "createdAt":"2018-04-25T12:00:24.331993Z"
}
```

