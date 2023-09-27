import unittest

from synthetic.validators import Validator, ValidationCode, ValidatorSet

class ValidatorTest(unittest.TestCase):
    def test_validator_instance_inits_with_test_and_resolve_optional_functions (self):
        validator1 = Validator(
            test=lambda x: True,
            resolve=lambda x: x
        )
        
        validator2 = Validator(
            test=lambda x: True
        )
        
        self.assertIsInstance(validator1, Validator)
        self.assertIsInstance(validator2, Validator)
        
    def test_validator_instance_has_validate_method_that_returns_str_and_code_tuple (self):
        validator = Validator(
            test=lambda x: True,
            resolve=lambda x: x
        )
        
        output = validator.validate("content")
        self.assertIsInstance(output[0], ValidationCode)
        self.assertIsInstance(output[1], str)
        
    def test_validator_instance_validate_method_returns_code_ok_and_same_str_if_test_passes (self):
        validator = Validator(
            test=lambda x: x == "content",
            resolve=lambda x: x + "extra text"
        )
        string = "content"
        code, out_str = validator.validate(string)
        
        self.assertEqual(code, ValidationCode.OK)
        self.assertEqual(out_str, string)
        
    def test_validator_instance_validate_method_returns_code_fail_and_same_str_if_test_fails_and_no_resolve (self):
        validator = Validator(
            test=lambda x: False,
        )
        
        string = "content"
        code, out_str = validator.validate(string)
        
        self.assertEqual(code, ValidationCode.FAIL)
        self.assertEqual(out_str, string)
        
    def test_validator_instance_validate_method_returns_code_fail_and_same_str_if_test_fails_and_resolve_function_raises_exception (self):
        def resolve (string:str) -> str :
            raise Exception("Sample exception")
        
        validator = Validator(
            test=lambda x: False,
            resolve=resolve
        )
        
        string = "content"
        code, out_str = validator.validate(string)
        
        self.assertEqual(code, ValidationCode.FAIL)
        self.assertEqual(out_str, string)
        
    def test_validator_instance_validate_method_returns_code_fail_and_same_str_if_test_fails_and_no_resolve (self):
        validator = Validator(
            test=lambda x: False,
            resolve=lambda x: "Hello " + x
        )
        
        string = "Carlos"
        code, out_str = validator.validate(string)
        
        self.assertEqual(code, ValidationCode.WARN)
        self.assertEqual(out_str, "Hello " + string)
        
    def test_validator_set_can_be_init_passing_a_list_of_validators (self):
        validators_list = [Validator(test=lambda x: False), Validator(test=lambda x: True)]
        
        validator_set = ValidatorSet(validators_list)
        
        self.assertIsInstance(validator_set, ValidatorSet)
        
    def test_validator_set_valide_method_returns_tuple_of_validation_code_and_str (self) :
        validators_list = [Validator(test=lambda x: False), Validator(test=lambda x: True)]
        validator_set = ValidatorSet(validators_list)
        
        code, new_str = validator_set.validate("sample")
        self.assertIsInstance(code, ValidationCode)
        self.assertIsInstance(new_str, str)
        
    def test_validator_set_validate_method_returns_code_ok_and_same_str_if_all_tests_pass (self) :
        validators_list = [Validator(test=lambda x: True), Validator(test=lambda x: True)]
        validator_set = ValidatorSet(validators_list)
        
        string = "sample"
        code, new_str = validator_set.validate(string)
        self.assertEqual(code, ValidationCode.OK)
        self.assertEqual(new_str, string)
        
    def test_validator_set_validate_method_returns_code_fail_if_one_test_fails (self):
        validators_list = [Validator(test=lambda x: True), Validator(test=lambda x: False), Validator(test=lambda x: True)]
        validator_set = ValidatorSet(validators_list)
        
        string = "sample"
        code, _ = validator_set.validate(string)
        self.assertEqual(code, ValidationCode.FAIL)

    def test_validator_set_validate_method_returns_code_warn_if_one_test_warns_and_updates_str (self):
        validators_list = [Validator(test=lambda x: True), Validator(test=lambda x: False, resolve=lambda x: "Hello "+x), Validator(test=lambda x: "Hello Carlos" == x)]
        validator_set = ValidatorSet(validators_list)
        
        string = "Carlos"
        code, new_str = validator_set.validate(string)
        self.assertEqual(code, ValidationCode.WARN)
        self.assertEqual(new_str, "Hello " + string)
        
    def test_validator_set_validator_method_returns_code_fail_and_update_str_if_one_validation_warns_and_then_fails (self):
        validators_list = [Validator(test=lambda x: True), Validator(test=lambda x: False, resolve=lambda x: "Hello "+x), Validator(test=lambda x: False)]
        validator_set = ValidatorSet(validators_list)
        
        string = "Carlos"
        code, new_str = validator_set.validate(string)
        self.assertEqual(code, ValidationCode.FAIL)
        self.assertEqual(new_str, "Hello " + string)