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
    "phone":989122451075,
    "modifiedAt":null,
    "secret":"k2D7Pwr3spJFB1ZAhM6k46Tb1SbU7WXbrAe6Kf82+Cg=\n",
    "createdAt":"2018-05-06T12:39:48.738461Z"
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
    "modifiedAt":"2018-05-06T12:39:48.859635Z",
    "secret":"Yf3c22WrAY5spMGd5Gfh0rnmJXU6VOz7q3J9nRTHrhI=\n",
    "createdAt":"2018-05-06T12:39:48.738461Z"
}
```

