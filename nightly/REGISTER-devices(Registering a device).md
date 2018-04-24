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
```

```{
    "modifiedAt":null,
    "phone":989122451075,
    "secret":"bkfDteSgzSA36uxjc04DYjdoZXgRSaljGk2end4gA1Y=\n",
    "createdAt":"2018-04-24T22:53:57.076337Z"
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
    "modifiedAt":"2018-04-24T22:53:57.198523Z",
    "phone":989122451075,
    "secret":"RjUTZDSokDJEJhjuqNzSgpWilkWy1L4Ludj\/yXY+Ha4=\n",
    "createdAt":"2018-04-24T22:53:57.076337Z"
}
```

