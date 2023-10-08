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
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Return next response"""
        response = self.responses[self.i]
        if self.i < len(self.responses) - 1:
            self.i += 1
        else:
            self.i = 0
        
        if stop :
            for s in stop :
                try :
                    match = re.search(string=response, pattern=s)
                except re.error as e :
                    raise synthetic.RegexError(e)
                if match is not None :
                    idx = match.end()
                    response = response[:idx]
        
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
