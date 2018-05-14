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
    "expireDate":"2021-02-16",
    "isExpired":false,
    "createdAt":"2018-05-14T19:40:57.162035Z",
    "cryptomodule":{
        "timeInterval":60,
        "id":1,
        "oneTimePasswordLength":4
    },
    "phone":989122451075,
    "name":"DummyTokenName",
    "id":3,
    "modifiedAt":null,
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
    "expireDate":"2021-02-16",
    "isExpired":false,
    "createdAt":"2018-05-14T19:40:57.162035Z",
    "cryptomodule":{
        "timeInterval":60,
        "id":1,
        "oneTimePasswordLength":4
    },
    "phone":989122451075,
    "name":"DummyTokenName",
    "id":3,
    "modifiedAt":null,
    "isActive":true,
    "provisioning":"mt:\/\/oath\/totp\/DUMMYTOKENNAME468E16B1772442C701A2F0C468E1F722EC53B78112F9B1AD7C46425A2EAE3371043A34342C84A7CAFCF82298A12F3440012102163515"
}
```

