"""Customer CRUD + search + analyze routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request

from applications.api.dependencies import get_case_service, get_customer_service
from applications.api.exceptions import ApplicationsAPIError, ValidationAPIError
from applications.api.schemas.common import APIResponse
from applications.api.schemas.customer import (
    CustomerAnalyzeRequest,
    CustomerCreateRequest,
    CustomerUpdateRequest,
)
from applications.case_management.service import (
    CaseService,
    CaseServiceError,
)
from applications.customer.service import (
    CustomerNotFoundError,
    CustomerService,
    CustomerValidationError,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


def _not_found(customer_id: str) -> ApplicationsAPIError:
    return ApplicationsAPIError(
        f"Customer not found: {customer_id}",
        status_code=404,
        code="customer_not_found",
    )


@router.get("", response_model=APIResponse)
def list_customers(
    request: Request,
    name: str | None = Query(None),
    phone: str | None = Query(None),
    email: str | None = Query(None),
    tag: str | None = Query(None),
    created_from: str | None = Query(None),
    created_to: str | None = Query(None),
    service: CustomerService = Depends(get_customer_service),
) -> APIResponse:
    """List or search customers."""
    if any([name, phone, email, tag, created_from, created_to]):
        items = service.search(
            name=name,
            phone=phone,
            email=email,
            tag=tag,
            created_from=created_from,
            created_to=created_to,
        )
    else:
        items = service.list()
    return APIResponse(
        success=True,
        message="OK",
        data={"customers": [c.to_dict() for c in items], "count": len(items)},
        request_id=getattr(request.state, "request_id", None),
    )


@router.post("", response_model=APIResponse)
def create_customer(
    request: Request,
    body: CustomerCreateRequest,
    service: CustomerService = Depends(get_customer_service),
) -> APIResponse:
    """Create a customer."""
    try:
        customer = service.create(**body.model_dump())
    except CustomerValidationError as exc:
        raise ValidationAPIError(str(exc)) from exc
    return APIResponse(
        success=True,
        message="Customer created",
        data={"customer": customer.to_dict()},
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{customer_id}", response_model=APIResponse)
def get_customer(
    request: Request,
    customer_id: str,
    service: CustomerService = Depends(get_customer_service),
) -> APIResponse:
    """Get customer by id."""
    try:
        customer = service.get(customer_id)
    except CustomerNotFoundError as exc:
        raise _not_found(customer_id) from exc
    return APIResponse(
        success=True,
        message="OK",
        data={"customer": customer.to_dict()},
        request_id=getattr(request.state, "request_id", None),
    )


@router.put("/{customer_id}", response_model=APIResponse)
def update_customer(
    request: Request,
    customer_id: str,
    body: CustomerUpdateRequest,
    service: CustomerService = Depends(get_customer_service),
) -> APIResponse:
    """Update customer fields."""
    try:
        customer = service.update(
            customer_id,
            **body.model_dump(exclude_unset=True),
        )
    except CustomerNotFoundError as exc:
        raise _not_found(customer_id) from exc
    except CustomerValidationError as exc:
        raise ValidationAPIError(str(exc)) from exc
    return APIResponse(
        success=True,
        message="Customer updated",
        data={"customer": customer.to_dict()},
        request_id=getattr(request.state, "request_id", None),
    )


@router.delete("/{customer_id}", response_model=APIResponse)
def delete_customer(
    request: Request,
    customer_id: str,
    service: CustomerService = Depends(get_customer_service),
) -> APIResponse:
    """Delete a customer."""
    deleted = service.delete(customer_id)
    if not deleted:
        raise _not_found(customer_id)
    return APIResponse(
        success=True,
        message="Customer deleted",
        data={"customer_id": customer_id},
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{customer_id}/history", response_model=APIResponse)
def customer_history(
    request: Request,
    customer_id: str,
    case_service: CaseService = Depends(get_case_service),
) -> APIResponse:
    """List analysis history for a customer."""
    try:
        history = case_service.history(customer_id)
    except CustomerNotFoundError as exc:
        raise _not_found(customer_id) from exc
    return APIResponse(
        success=True,
        message="OK",
        data={"customer_id": customer_id, "history": history, "count": len(history)},
        request_id=getattr(request.state, "request_id", None),
    )


@router.post("/{customer_id}/analyze", response_model=APIResponse)
def analyze_customer(
    request: Request,
    customer_id: str,
    body: CustomerAnalyzeRequest | None = None,
    case_service: CaseService = Depends(get_case_service),
) -> APIResponse:
    """
    Run full engine pipeline for a customer and persist a Case.
    """
    overrides = None
    if body is not None:
        raw = body.model_dump(exclude_none=True)
        overrides = raw or None
    try:
        customer, case, pipeline = case_service.analyze_customer(
            customer_id,
            overrides=overrides,
        )
    except CustomerNotFoundError as exc:
        raise _not_found(customer_id) from exc
    except CaseServiceError as exc:
        raise ValidationAPIError(str(exc)) from exc

    return APIResponse(
        success=True,
        message="Analyze OK",
        data={
            "customer": customer.to_dict(),
            "case": case.to_dict(),
            "pipeline": pipeline,
        },
        request_id=getattr(request.state, "request_id", None),
    )
