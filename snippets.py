import os
import pytest

from ghosts.api_recorder.api_controller import ApiRecorderController
from ghosts.api_recorder.tests.scenario import (
    ApiSuperClassDecorated,
    scenario_val,
    api_response,
)

scenario_name = 'test_class_decorator'
