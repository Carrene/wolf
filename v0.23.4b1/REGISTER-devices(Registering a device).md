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
    "createdAt":"2018-04-25T11:57:42.249774Z",
    "secret":"yleT0ryIR327XrGOZ2NRnIW6I1gNRFM3Q4QBW1f9hh0=\n"
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
    "modifiedAt":"2018-04-25T11:57:42.420058Z",
    "createdAt":"2018-04-25T11:57:42.249774Z",
    "secret":"ylm+FjVB0HsbNApyCTeNV+crgcyy0gvqRJsrRFN0ois=\n"
}
```

