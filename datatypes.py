from typing import NamedTuple, List, Optional


class FieldValidationCheckNamedTuple(NamedTuple):
    is_valid: bool
    invalid_fields: Optional[List[str]] = None
    valid_fields: Optional[List[str]] = None
