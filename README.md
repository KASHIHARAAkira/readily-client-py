# readily_client_py

<!-- # Short Description -->

This is client library for Readily.

<!-- # Badges -->

[![Github issues](https://img.shields.io/github/issues/KASHIHARAAkira/readily_client_py)](https://github.com/KASHIHARAAkira/readily_client_py/issues)
[![Github forks](https://img.shields.io/github/forks/KASHIHARAAkira/readily_client_py)](https://github.com/KASHIHARAAkira/readily_client_py/network/members)
[![Github stars](https://img.shields.io/github/stars/KASHIHARAAkira/readily_client_py)](https://github.com/KASHIHARAAkira/readily_client_py/stargazers)
[![Github top language](https://img.shields.io/github/languages/top/KASHIHARAAkira/readily_client_py)](https://github.com/KASHIHARAAkira/readily_client_py/)
[![Github license](https://img.shields.io/github/license/KASHIHARAAkira/readily_client_py)](https://github.com/KASHIHARAAkira/readily_client_py/)

# Tags

`Readily` `IoT` `spreadsheet`

# Minimal Example


```
import readily_client_py

readily = readily_client_py.Readily("./cred.json")
data = [[0.12, 3.5, 9.8, 4.4]]
print(readily.upload(data, "375d8029aa9cc980731be8"))
```

# Contributors

- [KASHIHARAAkira](https://github.com/KASHIHARAAkira)
