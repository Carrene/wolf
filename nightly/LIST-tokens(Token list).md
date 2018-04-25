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
        "expireDate":"2099-12-07",
        "isExpired":false,
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.223722Z",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.226505Z",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"third_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "modifiedAt":null,
        "id":3,
        "phone":989121234568,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.227328Z",
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
        "expireDate":"2099-12-07",
        "isExpired":false,
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.223722Z",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.226505Z",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"third_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "modifiedAt":null,
        "id":3,
        "phone":989121234568,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.227328Z",
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
        "expireDate":"2018-04-24",
        "isExpired":true,
        "modifiedAt":null,
        "id":3,
        "phone":989121234568,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.227328Z",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.226505Z",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"first_token",
        "expireDate":"2099-12-07",
        "isExpired":false,
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.223722Z",
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
        "expireDate":"2099-12-07",
        "isExpired":false,
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.223722Z",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.226505Z",
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
        "expireDate":"2099-12-07",
        "isExpired":false,
        "modifiedAt":null,
        "id":1,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.223722Z",
        "isActive":true,
        "provisioning":null
    },
    {
        "name":"second_token",
        "expireDate":"2018-04-24",
        "isExpired":true,
        "modifiedAt":null,
        "id":2,
        "phone":989121234567,
        "cryptomodule":{
            "timeInterval":60,
            "oneTimePasswordLength":4,
            "id":1
        },
        "createdAt":"2018-04-25T09:05:36.226505Z",
        "isActive":true,
        "provisioning":null
    }
]
```

