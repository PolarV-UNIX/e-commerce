from django.core.validators import RegexValidator

class PhoneNumberValidator(RegexValidator):
    regex = '^98(9[0-3,9]\d{8}|[1-9]\d{9})$'
    message = 'phone number must be a VALID 12 digits like 98xxxxxxxxxx'
    code = 'invalid_phone_number'

class SKUValidator(RegexValidator):
    regex = '^[a-zA-Z0-9]{6-20}$'
    message = 'SKU invalid'
    code = 'invalid sku'

class UsernameVlidator(RegexValidator):
    regex = '^[a-zA-Z][a-zA-Z0-9_\.]+$'
    message = 'enter username'
    code = "invalid_username"


class PostalCodeValidator(RegexValidator):
    regex = '^[0-9]{10}$'
    message = 'enter the postalcode'
    code = "invalid_postal_code"


class IDNumberValidator(RegexValidator):
    regex = '^[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0-16}$'
    message = 'enter the valid id'
    code = "invalid_id_number"


class BankCardNumberValidator(RegexValidator):
    regex = '^[0-9]{16}$'
    message = 'enter the valid cardname'
    code = "invalid_bank_card_number"


validator_phone_number = PhoneNumberValidator()
validator_sku = SKUValidator()
validator_username = UsernameVlidator()
validator_postal_code = PostalCodeValidator()
validator_id_number = IDNumberValidator()
validator_iban_number = IDNumberValidator()
validator_bank_card_number = BankCardNumberValidator()