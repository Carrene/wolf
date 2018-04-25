## Extend a token

### EXTEND /apiv1/tokens/:token_id

Extend a token by id

### Url Parameters

Name | Example
--- | ---
token_id | 1

### Form

Name | Example
--- | ---
expireDate | 1613434403

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 368

#### Body

```json
{
    "cryptomodule":{
        "oneTimePasswordLength":4,
        "timeInterval":60,
        "id":1
    },
    "name":"expired_token",
    "expireDate":"2021-02-16",
    "isExpired":false,
    "createdAt":"2018-04-25T11:31:18.950832Z",
    "phone":989121234567,
    "modifiedAt":"2018-04-25T11:31:18.967339Z",
    "id":1,
    "isActive":true,
    "provisioning":null
}
```

## WHEN: Trying extend a none existence token

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

## WHEN: Trying to extend a expired token to a time that passed

### Form

Name | Example
--- | ---
expireDate | 1513434403

### Response: 400 Bad Request

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 92

#### Body

```json
{"message":"Bad Request","description":"expireDate must be grater that current expireDate."}
```

## WHEN: Trying to extend a not expired token to a time that is less than its expire date

### Url Parameters

Name | Example
--- | ---
token_id | 2

### Form

Name | Example
--- | ---
expireDate | 1813434403

### Response: 400 Bad Request

#### Headers

* Content-Type: application/json; charset=utf-8
* Content-Length: 92

#### Body

```json
{"message":"Bad Request","description":"expireDate must be grater that current expireDate."}
```

## WHEN: Trying to extend a token with a un supported expireDate format

### Form

Name | Example
--- | ---
expireDate | 2019-12-07T18:14:39.558891

### Response: 400 Bad Request

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Reason: invalid-expireDate-type
* Content-Length: 77

#### Body

```json
{"message":"Bad Request","description":"The field: expireDate must be float"}
```

