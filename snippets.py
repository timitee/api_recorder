import os
import pytest

from ghosts.decorators.api_recorder import ApiRecorderController
from ghosts.decorators.tests.scenario import (
    ApiSuperClassDecorated,
    scenario_val,
    api_response,
)

scenario_name = 'test_class_decorator'
