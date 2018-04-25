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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "expireDate":"2099-12-07",
        "isExpired":false,
        "createdAt":"2018-04-25T11:31:19.730516Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":1,
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "createdAt":"2018-04-25T11:31:19.732181Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":2,
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"third_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "createdAt":"2018-04-25T11:31:19.732772Z",
        "phone":989121234568,
        "modifiedAt":null,
        "id":3,
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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "expireDate":"2099-12-07",
        "isExpired":false,
        "createdAt":"2018-04-25T11:31:19.730516Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":1,
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "createdAt":"2018-04-25T11:31:19.732181Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":2,
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"third_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "createdAt":"2018-04-25T11:31:19.732772Z",
        "phone":989121234568,
        "modifiedAt":null,
        "id":3,
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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"third_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "createdAt":"2018-04-25T11:31:19.732772Z",
        "phone":989121234568,
        "modifiedAt":null,
        "id":3,
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "createdAt":"2018-04-25T11:31:19.732181Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":2,
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "expireDate":"2099-12-07",
        "isExpired":false,
        "createdAt":"2018-04-25T11:31:19.730516Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":1,
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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "expireDate":"2099-12-07",
        "isExpired":false,
        "createdAt":"2018-04-25T11:31:19.730516Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":1,
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "createdAt":"2018-04-25T11:31:19.732181Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":2,
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
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"first_token",
        "expireDate":"2099-12-07",
        "isExpired":false,
        "createdAt":"2018-04-25T11:31:19.730516Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":1,
        "isActive":true,
        "provisioning":null
    },
    {
        "cryptomodule":{
            "oneTimePasswordLength":4,
            "timeInterval":60,
            "id":1
        },
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "createdAt":"2018-04-25T11:31:19.732181Z",
        "phone":989121234567,
        "modifiedAt":null,
        "id":2,
        "isActive":true,
        "provisioning":null
    }
]
```

