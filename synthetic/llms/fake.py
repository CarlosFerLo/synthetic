from typing import Optional, List, Any, Mapping
from langchain.llms.base import LLM

import re
import synthetic


class FakeLLM(LLM):
    """Fake LLM for testing purposes."""

    responses: List[str]
    sleep: Optional[float] = None
    i: int = 0

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "fake-list"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str | re.Pattern]] = None,
        **kwargs: Any,
    ) -> str:
        response = self.responses[self.i]
        if self.i < len(self.responses) - 1:
            self.i += 1
        else:
            self.i = 0

        if stop:
            for i in range(len(response), -1, -1):  # start from the end of the string
                substring = response[:i]
                for pattern in stop:
                    # Remove the $ character from the pattern
                    try :
                        if type(pattern) is str :
                            pattern = pattern.rstrip("$")
                        else :
                            pattern = pattern.pattern.rstrip("$")
                        match = re.search(pattern, substring)
                        if match is not None:
                            response = substring[:match.end()]
                            return response  # return as soon as a match is found
                    except re.error as e:
                        raise synthetic.RegexError(e)
                        

        return response
    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Return next response"""
        response = self.responses[self.i]
        if self.i < len(self.responses) - 1:
            self.i += 1
        else:
            self.i = 0
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"responses": self.responses}
