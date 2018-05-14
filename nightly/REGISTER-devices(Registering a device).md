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
    "secret":"KAcsOV89pT+l15qtH5CzT3H+35a+OMdm8GVNcszDx1M=\n",
    "modifiedAt":null,
    "createdAt":"2018-05-14T19:40:56.649479Z",
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
    "secret":"77iBGSw4EASZGiiEYRt2WdHXO6RWntmiTtPlvKoB8zY=\n",
    "modifiedAt":"2018-05-14T19:40:56.773035Z",
    "createdAt":"2018-05-14T19:40:56.649479Z",
    "phone":989122451075
}
```

