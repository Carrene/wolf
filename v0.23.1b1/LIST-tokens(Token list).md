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
        "name":"first_token",
        "isExpired":false,
        "expireDate":"2099-12-07",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.644626Z",
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "isExpired":true,
        "expireDate":"2018-04-24",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.646258Z",
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"third_token",
        "isExpired":true,
        "expireDate":"2018-04-24",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.646815Z",
        "modifiedAt":null,
        "id":3,
        "phone":989121234568,
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
        "name":"first_token",
        "isExpired":false,
        "expireDate":"2099-12-07",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.644626Z",
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "isExpired":true,
        "expireDate":"2018-04-24",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.646258Z",
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"third_token",
        "isExpired":true,
        "expireDate":"2018-04-24",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.646815Z",
        "modifiedAt":null,
        "id":3,
        "phone":989121234568,
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
        "name":"third_token",
        "isExpired":true,
        "expireDate":"2018-04-24",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.646815Z",
        "modifiedAt":null,
        "id":3,
        "phone":989121234568,
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "isExpired":true,
        "expireDate":"2018-04-24",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.646258Z",
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"first_token",
        "isExpired":false,
        "expireDate":"2099-12-07",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.644626Z",
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
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
        "name":"first_token",
        "isExpired":false,
        "expireDate":"2099-12-07",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.644626Z",
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "isExpired":true,
        "expireDate":"2018-04-24",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.646258Z",
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
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
        "name":"first_token",
        "isExpired":false,
        "expireDate":"2099-12-07",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.644626Z",
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "isExpired":true,
        "expireDate":"2018-04-24",
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "createdAt":"2018-04-25T11:18:23.646258Z",
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "isActive":true,
        "provisioning":null
    }
]
```

