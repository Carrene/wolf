## Token list

### LIST /apiv1/tokens

List of tokens

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 100
* X-Pagination-Skip: 0
* X-Pagination-Count: 3
* Content-Length: 1222

#### Body

```json
[
    {
        "modifiedAt":null,
        "name":"first_token",
        "id":1,
        "phone":989121234567,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T12:00:27.652246Z",
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "name":"second_token",
        "id":2,
        "phone":989121234567,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T12:00:27.654739Z",
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "name":"third_token",
        "id":3,
        "phone":989121234568,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T12:00:27.655642Z",
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    }
]
```

## WHEN: Trying to get list of tokens sorted by id ascending

### Query Strings

Name | Example
--- | ---
sort | id

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 100
* X-Pagination-Skip: 0
* X-Pagination-Count: 3
* Content-Length: 1222

#### Body

```json
[
    {
        "modifiedAt":null,
        "name":"first_token",
        "id":1,
        "phone":989121234567,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T12:00:27.652246Z",
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "name":"second_token",
        "id":2,
        "phone":989121234567,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T12:00:27.654739Z",
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "name":"third_token",
        "id":3,
        "phone":989121234568,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T12:00:27.655642Z",
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    }
]
```

## WHEN: Trying to get list of tokens sorted by id descending

### Query Strings

Name | Example
--- | ---
sort | -id

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 100
* X-Pagination-Skip: 0
* X-Pagination-Count: 3
* Content-Length: 1222

#### Body

```json
[
    {
        "modifiedAt":null,
        "name":"third_token",
        "id":3,
        "phone":989121234568,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T12:00:27.655642Z",
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "name":"second_token",
        "id":2,
        "phone":989121234567,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T12:00:27.654739Z",
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "name":"first_token",
        "id":1,
        "phone":989121234567,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T12:00:27.652246Z",
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    }
]
```

## WHEN: Trying to get list of tokens with phone query string

### Query Strings

Name | Example
--- | ---
phone | 989121234567

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 100
* X-Pagination-Skip: 0
* X-Pagination-Count: 2
* Content-Length: 816

#### Body

```json
[
    {
        "modifiedAt":null,
        "name":"first_token",
        "id":1,
        "phone":989121234567,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T12:00:27.652246Z",
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "name":"second_token",
        "id":2,
        "phone":989121234567,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T12:00:27.654739Z",
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    }
]
```

## WHEN: Trying to get list of tokens with take query string

### Query Strings

Name | Example
--- | ---
take | 2

### Response: 200 OK

#### Headers

* Content-Type: application/json; charset=utf-8
* X-Pagination-Take: 2
* X-Pagination-Skip: 0
* X-Pagination-Count: 3
* Content-Length: 816

#### Body

```json
[
    {
        "modifiedAt":null,
        "name":"first_token",
        "id":1,
        "phone":989121234567,
        "expireDate":"2099-12-07",
        "createdAt":"2018-04-25T12:00:27.652246Z",
        "isExpired":false,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    },
    {
        "modifiedAt":null,
        "name":"second_token",
        "id":2,
        "phone":989121234567,
        "expireDate":"2018-04-24",
        "createdAt":"2018-04-25T12:00:27.654739Z",
        "isExpired":true,
        "cryptomodule":{
            "id":1,
            "oneTimePasswordLength":4,
            "timeInterval":60
        },
        "isActive":true,
        "provisioning":null
    }
]
```

