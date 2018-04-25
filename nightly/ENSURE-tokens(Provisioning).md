## Provisioning

### ENSURE /apiv1/tokens

Provisioning

### Form

Name | Example
--- | ---
phone | 989122451075
name | DummyTokenName
cryptomoduleId | 1
expireDate | 1613434403

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 483

#### Body

```json
{
    "name":"DummyTokenName",
    "expireDate":"2021-02-16",
    "isExpired":false,
    "modifiedAt":null,
    "id":3,
    "phone":989122451075,
    "cryptomodule":{
        "timeInterval":60,
        "oneTimePasswordLength":4,
        "id":1
    },
    "createdAt":"2018-04-25T09:05:34.579729Z",
    "isActive":true,
    "provisioning":"mt:\/\/oath\/totp\/DUMMYTOKENNAME468E16B1772442C701A2F0C468E1F722EC53B78112F9B1AD7C46425A2EAE3371043A34342C84A7CAFCF82298A12F3440012102163515"
}
```

## WHEN: Ensure the same token again

### Form

Name | Example
--- | ---
phone | 989122451075
name | DummyTokenName
cryptomoduleId | 1
expireDate | 1513434403

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 483

#### Body

```json
{
    "name":"DummyTokenName",
    "expireDate":"2021-02-16",
    "isExpired":false,
    "modifiedAt":null,
    "id":3,
    "phone":989122451075,
    "cryptomodule":{
        "timeInterval":60,
        "oneTimePasswordLength":4,
        "id":1
    },
    "createdAt":"2018-04-25T09:05:34.579729Z",
    "isActive":true,
    "provisioning":"mt:\/\/oath\/totp\/DUMMYTOKENNAME468E16B1772442C701A2F0C468E1F722EC53B78112F9B1AD7C46425A2EAE3371043A34342C84A7CAFCF82298A12F3440012102163515"
}
```

