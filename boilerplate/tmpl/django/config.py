from boilerplate import Configuration
from random import choice


conf = Configuration(__file__, {
    'secret_key': ''.join([
        choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)
    ]),
})
