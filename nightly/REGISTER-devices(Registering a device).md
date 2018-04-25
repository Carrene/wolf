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
    "phone":989122451075,
    "createdAt":"2018-04-25T09:05:32.537203Z",
    "modifiedAt":null,
    "secret":"qW2pzm9ATvG17YmCh\/9+UYGEyZ7tlxZJJeE1VhWibBw=\n"
}
```

## WHEN: Trying to registering the same device again

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 188

#### Body

```json
{
    "phone":989122451075,
    "createdAt":"2018-04-25T09:05:32.537203Z",
    "modifiedAt":"2018-04-25T09:05:32.716288Z",
    "secret":"S8JYo4tuFIABY5ZSQPl+tBsv9mGtb5BMJ8\/v8j\/2fQI=\n"
}
```

