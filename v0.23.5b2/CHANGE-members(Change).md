## Change

### CHANGE /apiv1/members/:member_id/password

Change Password

### Url Parameters

Name | Example
--- | ---
member_id | 1

### Form

Name | Example
--- | ---
currentPassword | 123456
newPassword | 1234567

### Request Headers

* AUTHORIZATION: eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyNDc1NjEwNywiZXhwIjoxNTI0ODQyNTA3fQ.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGVzIjpbImFkbWluIl0sInNlc3Npb25JZCI6ImNlMzM2NTlmLTIzMzEtNDAxNC04YTEzLTdmNDE3NmI5NGQ2YiJ9.BJAi9L5hWCxFjrriG2blwYJr-TX0zVk8IGEp6mAEFBA

### Response: 200 OK

#### Headers

* X-Identity: 1
* Content-Type: application/json; charset=utf-8
* Content-Length: 4

#### Body

```json
{

}
```

## WHEN: Trying to change password with wrong current password

### Form

Name | Example
--- | ---
currentPassword | invalid

### Response: 400 Bad Request

#### Headers

* X-Identity: 1
* Content-Type: application/json; charset=utf-8
* X-Reason: invalid-newPassword
* Content-Length: 106

#### Body

```json
{"message":"Bad Request","description":"Exactly these fields are allowed: [currentPassword, newPassword]"}
```

## WHEN: Trying to change another user password

### Url Parameters

Name | Example
--- | ---
member_id | 999

### Response: 403 Forbidden

#### Headers

* X-Identity: 1
* Content-Type: application/json; charset=utf-8
* Content-Length: 88

#### Body

```json
{"message":"Forbidden","description":"Request forbidden -- authorization will not help"}
```
