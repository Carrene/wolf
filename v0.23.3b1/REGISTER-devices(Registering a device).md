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
{
    "secret":"RdTwDPtA6oQ1pUAC\/bf2oANap9Ar0wqvpV8ErSK5KXo=\n",
    "modifiedAt":null,
    "createdAt":"2018-04-25T11:28:33.329419Z",
    "phone":989122451075
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
    "secret":"yTORiBiukF7Ed5tjJ7cwpvmxKRdO\/LGK5UsHLqv0xzw=\n",
    "modifiedAt":"2018-04-25T11:28:33.461034Z",
    "createdAt":"2018-04-25T11:28:33.329419Z",
    "phone":989122451075
}
```

