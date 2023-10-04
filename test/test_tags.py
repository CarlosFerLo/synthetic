import unittest 

from synthetic.tags import Tag
from synthetic.validators import ValidatorSet

class TagsTest (unittest.TestCase) :
    def test_tag_init_with_name_str_property (self):
        tag = Tag(name="name")
        
        self.assertIsInstance(tag, Tag)
        self.assertEqual(tag.name, "name")
        
    def test_tag_can_be_init_with_validator_set (self) :
        tag = Tag(name="name", validator_set=ValidatorSet(validators=[]))
        
        self.assertIsInstance(tag, Tag)
        self.assertIsInstance(tag.validator_set, ValidatorSet)
        
    
        
        