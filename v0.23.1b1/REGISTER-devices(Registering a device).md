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
    "createdAt":"2018-04-25T11:18:20.694610Z",
    "modifiedAt":null,
    "secret":"5ZtFHFWRKuisS\/Wql76A4qvN+X+WL+1JFTb1+dSeVvU=\n",
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
    "createdAt":"2018-04-25T11:18:20.694610Z",
    "modifiedAt":"2018-04-25T11:18:20.807135Z",
    "secret":"xRG1jPlBswvTKCH82ACYrlPgFcSVJkVaOR40Lb1VNBM=\n",
    "phone":989122451075
}
```

