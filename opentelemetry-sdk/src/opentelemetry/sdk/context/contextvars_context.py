# Copyright 2020, OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from contextvars import ContextVar
from sys import version_info

from opentelemetry.context import Context
from opentelemetry.context.context import RuntimeContext

if (3, 5, 3) <= version_info < (3, 7):
    import aiocontextvars  # type: ignore # pylint:disable=unused-import

elif (3, 4) < version_info <= (3, 5, 2):
    import opentelemetry.sdk.context.aiocontextvarsfix  # pylint:disable=unused-import


class ContextVarsRuntimeContext(RuntimeContext):
    """An implementation of the RuntimeContext interface which wraps ContextVar under
    the hood. This is the prefered implementation for usage with Python 3.5+
    """

    _CONTEXT_KEY = "current_context"

    def __init__(self) -> None:
        self._current_context = ContextVar(
            self._CONTEXT_KEY, default=Context()
        )

    def set_current(self, context: Context) -> None:
        """See `opentelemetry.context.RuntimeContext.set_current`."""
        self._current_context.set(context)

    def get_current(self) -> Context:
        """See `opentelemetry.context.RuntimeContext.get_current`."""
        return self._current_context.get()


__all__ = ["ContextVarsRuntimeContext"]