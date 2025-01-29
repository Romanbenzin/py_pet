import allure
from assertpy import assert_that


class Assertions:
    @staticmethod
    def assert_that_value_is_equal_to(
        field_name,
        actual_value,
        expected_value,
        description="",
    ):
        step_description = (
            f"Сравниваем, что [{field_name}] \nравен [{expected_value}]"
        )
        with allure.step(step_description):
            assert_that(actual_value, description).is_equal_to(expected_value)
