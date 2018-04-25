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
    "name":"deactive_token",
    "expireDate":"2099-12-07",
    "isExpired":false,
    "modifiedAt":"2018-04-25T09:05:32.984703Z",
    "id":2,
    "phone":989121234567,
    "cryptomodule":{
        "timeInterval":60,
        "oneTimePasswordLength":4,
        "id":1
    },
    "createdAt":"2018-04-25T09:05:32.969598Z",
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
