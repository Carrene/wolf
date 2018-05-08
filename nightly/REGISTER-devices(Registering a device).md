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
    "phone":989122451075,
    "modifiedAt":null,
    "secret":"\/p6DEOxoBEYp5K\/xSEGeJ8zEJXaILhDlFedYRPJ49p4=\n",
    "createdAt":"2018-05-08T08:05:13.116509Z"
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
    "modifiedAt":"2018-05-08T08:05:13.235498Z",
    "secret":"3cK2vY1chwigYQNYY7lEe5JevCcwmu93GhGbbaYVfog=\n",
    "createdAt":"2018-05-08T08:05:13.116509Z"
}
```

