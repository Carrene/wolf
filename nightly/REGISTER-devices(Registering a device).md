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
    "createdAt":"2018-04-24T23:31:39.994084Z",
    "phone":989122451075,
    "secret":"8G6AaZmjXLW+DDFf8+GPRhfvZZTLumrRJp+LabqEwzk=\n",
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
    "createdAt":"2018-04-24T23:31:39.994084Z",
    "phone":989122451075,
    "secret":"7E\/mmk1cRmpOy+iYRmONe+fBMgKLtzCiWqX17kkZzNk=\n",
    "modifiedAt":"2018-04-24T23:31:40.124375Z"
}
```

