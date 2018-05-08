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
    "createdAt":"2018-05-08T09:16:58.495364Z",
    "modifiedAt":null,
    "phone":989122451075,
    "secret":"SmE1a24v0C2l5fgVvPUCthrD4EFqMd9g6TThr8AYMtI=\n"
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
    "createdAt":"2018-05-08T09:16:58.495364Z",
    "modifiedAt":"2018-05-08T09:16:58.612268Z",
    "phone":989122451075,
    "secret":"RMbM1vzSBVo9Y29Oe68Hk49NKDs3OZ7jDvesTKkLnSY=\n"
}
```

