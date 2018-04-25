## Deactivate a token

### DEACTIVATE /apiv1/tokens/:token_id

Deactivate a token by id

### Url Parameters

Name | Example
--- | ---
token_id | 1

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 367

#### Body

```json
{
    "name":"active_token",
    "isExpired":true,
    "expireDate":"2000-12-07",
    "cryptomodule":{
        "oneTimePasswordLength":4,
        "timeInterval":60,
        "id":1
    },
    "createdAt":"2018-04-25T11:18:21.607058Z",
    "modifiedAt":"2018-04-25T11:18:21.616591Z",
    "id":1,
    "phone":989121234567,
    "isActive":false,
    "provisioning":null
}
```

## WHEN: Trying to deactivate a none existence token

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

## WHEN: Trying to deactivate a active token

### Url Parameters

Name | Example
--- | ---
token_id | 2

### Response: 463 Token is deactivated

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 78

#### Body

```json
{"message":"Token is deactivated","description":"Token has been deactivated."}
```

