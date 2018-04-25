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
    "secret":"axXWwGKyOdR17D0yVi2YHVv6P9XqM+VabzXokG7i+do=\n",
    "phone":989122451075,
    "modifiedAt":null,
    "createdAt":"2018-04-25T11:31:16.399882Z"
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
    "secret":"DZ9VUB4lebEfZYuAtb0GXujBad+jYe4ZFExKmeWxaHc=\n",
    "phone":989122451075,
    "modifiedAt":"2018-04-25T11:31:16.531271Z",
    "createdAt":"2018-04-25T11:31:16.399882Z"
}
```

