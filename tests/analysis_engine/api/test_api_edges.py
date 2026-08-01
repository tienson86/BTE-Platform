"""Additional API facade edge-case tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.api.analysis_engine import AnalysisEngineAPI
from engines.analysis_engine.api.analysis_request import AnalysisRequest
from engines.analysis_engine.api.analysis_response import (
    AnalysisResponse,
    AnalysisResponseStatus,
)
from engines.analysis_engine.api.analysis_session import AnalysisSessionStatus
from engines.analysis_engine.exceptions.runtime_error import AnalysisRuntimeError
from engines.analysis_engine.results.result_builder import ResultBuilder


class TestApiFacadeEdges:
    """Extra coverage for API session and response validation edges."""

    def test_session_bind_and_close_guards(self) -> None:
        """Closed sessions should reject further binds."""
        api = AnalysisEngineAPI()
        session = api.open_session(pipeline_id="p")
        session.bind_request(AnalysisRequest(pipeline_id="p"))
        assert session.status == AnalysisSessionStatus.BOUND
        api.close_session(session.session_id)
        with pytest.raises(AnalysisRuntimeError):
            session.bind_request(AnalysisRequest(pipeline_id="p"))
        with pytest.raises(AnalysisRuntimeError):
            api.service.get_session("missing")

    def test_finalize_service_and_response_validate(self) -> None:
        """Finalize facade and response validation helpers should work."""
        api = AnalysisEngineAPI()
        analysis = (
            ResultBuilder()
            .with_id("ar")
            .with_pipeline_id("p")
            .with_success(True)
            .build_analysis_result()
        )
        response = api.service.finalize(analysis, request_id="req-1")
        assert response.status == AnalysisResponseStatus.FINALIZED
        assert response.validate() is True
        invalid = AnalysisResponse(
            request_id="",
            success=True,
            status=AnalysisResponseStatus.FAILED,
        )
        assert invalid.validate() is False
