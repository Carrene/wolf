## Activate a token

### ACTIVATE /apiv1/tokens/:token_id

Activate a token by id

### Url Parameters

Name | Example
--- | ---
token_id | 2

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 369

#### Body

```json
{
    "modifiedAt":"2018-04-25T12:00:24.897996Z",
    "name":"deactive_token",
    "id":2,
    "phone":989121234567,
    "expireDate":"2099-12-07",
    "createdAt":"2018-04-25T12:00:24.881319Z",
    "isExpired":false,
    "cryptomodule":{
        "id":1,
        "oneTimePasswordLength":4,
        "timeInterval":60
    },
    "isActive":true,
    "provisioning":null
}
```

## WHEN: Trying to activate a none existence token

### Url Parameters

Name | Example
--- | ---
token_id | 0

### Response: 404 Not Found

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 69

#### Body

```json
{"message":"Not Found","description":"Nothing matches the given URI"}
```

## WHEN: Trying to activate a active token

### Url Parameters

Name | Example
--- | ---
token_id | 1

### Response: 465 Token is active

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 70

#### Body

```json
{"message":"Token is active","description":"Token is already active."}
```

