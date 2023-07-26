# IntegraCommerce API Client

This project provides a Python API client for interacting with the IntegraCommerce platform. It allows you to seamlessly integrate your application with IntegraCommerce, enabling the synchronization of data, managing orders, updating inventory, and more.

# TODO
Create the server to deal with the webhooks in SOAP
## FILES
```bash
├── app.py
├── client.py
├── customer.py
├── __init__.py
├── __pycache__
│   ├── app.cpython-310.pyc
│   ├── client.cpython-310.pyc
│   ├── customer.cpython-310.pyc
│   └── __init__.cpython-310.pyc
├── README.md
├── requests.http
├── resources
│   ├── catalog
│   │   ├── brand.py
│   │   ├── category.py
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── __pycache__
│   │   │   ├── brand.cpython-310.pyc
│   │   │   ├── category.cpython-310.pyc
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── product.cpython-310.pyc
│   │   │   └── supplier.cpython-310.pyc
│   │   └── supplier.py
│   ├── customer
│   │   ├── customer.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── customer.cpython-310.pyc
│   │       └── __init__.cpython-310.pyc
│   ├── __init__.py
│   ├── inventories
│   │   ├── __init__.py
│   │   ├── inventories.py
│   │   └── __pycache__
│   │       ├── __init__.cpython-310.pyc
│   │       └── inventories.cpython-310.pyc
│   ├── orders
│   │   ├── __init__.py
│   │   └── order.py
│   ├── protocols
│   │   ├── protocols.py
│   │   └── __pycache__
│   │       └── protocols.cpython-310.pyc
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   └── resource.cpython-310.pyc
│   ├── resource.py
│   └── tracking
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-310.pyc
│       │   └── tracking.cpython-310.pyc
│       └── tracking.py
├── servers
│   ├── REST
│   └── SOAP
│       └── soap.py
├── swagger.yml
├── templates
│   └── home.html
└── tests
    └── test_data.py
```
## Installation
    ---------------

## Usage
    ---------------

## Contributing

Contributions to this project are always welcome. If you find a bug, have a feature request, or want to suggest an improvement, please create an issue in the GitHub repository.

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Submit a pull request.

Please ensure that your code adheres to the existing coding style and includes appropriate tests.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
