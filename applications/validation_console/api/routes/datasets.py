"""Dataset CRUD, import, compare, stats, coverage."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request

from applications.validation_console.api.schemas import (
    APIEnvelope,
    AddCaseRequest,
    CreateDatasetRequest,
    ImportDatasetRequest,
    SetActualRequest,
)
from applications.validation_console.api.services import (
    GoldenDatasetService,
    NotFoundError,
    ValidationConsoleError,
    ValidationError,
    WorkflowError,
)

router = APIRouter(tags=["Datasets"])


def _service() -> GoldenDatasetService:
    return GoldenDatasetService()


def _envelope(request: Request, *, message: str, data: object) -> APIEnvelope:
    return APIEnvelope(
        success=True,
        message=message,
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )


def _http_error(exc: ValidationConsoleError) -> HTTPException:
    if isinstance(exc, NotFoundError):
        return HTTPException(
            status_code=404,
            detail={"message": exc.message, **exc.details},
        )
    if isinstance(exc, ValidationError):
        return HTTPException(
            status_code=422,
            detail={
                "message": exc.message,
                "issues": [issue.to_dict() for issue in exc.issues],
                **exc.details,
            },
        )
    if isinstance(exc, WorkflowError):
        return HTTPException(
            status_code=409,
            detail={"message": exc.message, **exc.details},
        )
    return HTTPException(
        status_code=400,
        detail={"message": exc.message, **exc.details},
    )


@router.get("/datasets")
def list_datasets(
    request: Request,
    status: str | None = Query(default=None),
    module: str | None = Query(default=None),
) -> APIEnvelope:
    """List managed golden datasets."""
    data = _service().list_datasets(status=status, module=module)
    return _envelope(request, message="OK", data=data)


@router.post("/datasets")
def create_dataset(request: Request, body: CreateDatasetRequest) -> APIEnvelope:
    """Create a draft golden dataset."""
    try:
        data = _service().create_dataset(
            name=body.name,
            description=body.description,
            module=body.module,
            cases=body.cases,
            actor=body.actor,
            metadata=body.metadata,
        )
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Created", data=data)


@router.post("/datasets/import")
def import_dataset(request: Request, body: ImportDatasetRequest) -> APIEnvelope:
    """Import a dataset bundle."""
    try:
        data = _service().import_dataset(
            name=body.name,
            cases=body.cases,
            description=body.description,
            module=body.module,
            actor=body.actor,
            metadata=body.metadata,
        )
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Imported", data=data)


@router.get("/datasets/{dataset_id}")
def get_dataset(request: Request, dataset_id: str) -> APIEnvelope:
    """Read one dataset."""
    try:
        data = _service().get_dataset(dataset_id)
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)


@router.post("/datasets/{dataset_id}/cases")
def add_case(
    request: Request,
    dataset_id: str,
    body: AddCaseRequest,
) -> APIEnvelope:
    """Add a case to a draft dataset."""
    try:
        data = _service().add_case(
            dataset_id,
            case=body.case,
            actor=body.actor,
        )
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Case added", data=data)


@router.put("/datasets/{dataset_id}/cases/{case_id}/actual")
def set_actual(
    request: Request,
    dataset_id: str,
    case_id: str,
    body: SetActualRequest,
) -> APIEnvelope:
    """Attach actual output for a case."""
    try:
        data = _service().set_actual(
            dataset_id,
            case_id,
            actual_output=body.actual_output,
            actor=body.actor,
        )
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Actual set", data=data)


@router.get("/datasets/{dataset_id}/compare")
def compare_dataset(
    request: Request,
    dataset_id: str,
    case_id: str | None = Query(default=None),
) -> APIEnvelope:
    """Compare expected vs actual."""
    try:
        data = _service().compare(dataset_id, case_id=case_id)
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)


@router.get("/datasets/{dataset_id}/statistics")
def dataset_statistics(request: Request, dataset_id: str) -> APIEnvelope:
    """Return dataset statistics."""
    try:
        data = _service().statistics(dataset_id)
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)


@router.get("/datasets/{dataset_id}/coverage")
def dataset_coverage(request: Request, dataset_id: str) -> APIEnvelope:
    """Return coverage report."""
    try:
        data = _service().coverage(dataset_id)
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)
