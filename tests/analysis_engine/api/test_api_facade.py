"""Public API facade integration tests."""

from __future__ import annotations

from engines.analysis_engine.api.analysis_engine import AnalysisEngineAPI
from engines.analysis_engine.api.analysis_request import AnalysisRequest
from engines.analysis_engine.api.analysis_response import AnalysisResponseStatus
from engines.analysis_engine.context.context_factory import ContextFactory


class TestApiFacadeIntegration:
    """Integration coverage for architecture API facade (no BaZi rules)."""

    def test_analyze_request_and_finalize(self) -> None:
        """API facade should wire request → engine skeleton → response."""
        api = AnalysisEngineAPI()
        request = AnalysisRequest(
            pipeline_id="api_pipe",
            chart_id="chart_mock",
            attributes={"mock": True},
            finalize=True,
        )
        assert api.validate_request(request) is True
        response = api.analyze_request(request)
        assert response.success is True
        assert response.status == AnalysisResponseStatus.FINALIZED
        assert response.analysis_result is not None
        assert response.final_result is not None
        assert response.validate() is True

        final = api.finalize(response.analysis_result)
        assert final.pipeline_id == "api_pipe"

    def test_session_lifecycle(self) -> None:
        """API sessions should track request/response without business logic."""
        api = AnalysisEngineAPI()
        session = api.open_session(pipeline_id="session_pipe")
        request = AnalysisRequest(
            pipeline_id="session_pipe",
            session_id=session.session_id,
        )
        response = api.service.analyze(request, session=session)
        assert response.session_id == session.session_id
        assert session.response is not None
        assert session.describe()["pipeline_id"] == "session_pipe"
        api.close_session(session.session_id)

    def test_interface_analyze_and_validate_context(self) -> None:
        """AnalysisEngineInterface methods should work via facade."""
        api = AnalysisEngineAPI()
        context = ContextFactory().create(
            pipeline_id="iface_pipe",
            context_id="iface_ctx",
        )
        assert api.validate_context(context) is True
        result = api.analyze(context)
        assert result.success is True
        assert result.pipeline_id == "iface_pipe"

    def test_invalid_request_returns_invalid_status(self) -> None:
        """Invalid requests should fail structurally at the facade."""
        api = AnalysisEngineAPI()
        response = api.analyze_request(AnalysisRequest(pipeline_id=""))
        assert response.success is False
        assert response.status == AnalysisResponseStatus.INVALID
