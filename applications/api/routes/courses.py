"""Authenticated course catalog, access, protected video and Admin configuration."""
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from applications.api.auth.dependencies import CurrentUser
from applications.api.dependencies import get_auth_service
from applications.api.schemas.courses import CourseSettings, CourseRedeem, LessonProgress, CourseCreate, LessonEdit
from applications.api.services.courses import CourseService, MEDIA_PATH, fail

router = APIRouter(tags=["Courses"])


def service():
    return CourseService(get_auth_service().store)


@router.get("/courses")
def catalog(user: CurrentUser, svc=Depends(service)):
    return svc.catalog(user)


@router.get("/admin/courses")
def admin_catalog(user: CurrentUser, svc=Depends(service)):
    return svc.catalog(user, management=True)


@router.post("/admin/courses", status_code=201)
def create(body: CourseCreate, user: CurrentUser, svc=Depends(service)):
    return svc.create(user, body)


@router.get("/admin/courses/{course_id}/lessons")
def admin_lessons(course_id: str, user: CurrentUser, svc=Depends(service)):
    return svc.lesson_catalog(user, course_id)


@router.post("/admin/courses/{course_id}/lessons", status_code=201)
def add_lesson(course_id: str, body: LessonEdit, user: CurrentUser, svc=Depends(service)):
    return svc.save_lesson(user, course_id, body)


@router.put("/admin/courses/{course_id}/lessons/{lesson_id}")
def edit_lesson(course_id: str, lesson_id: str, body: LessonEdit, user: CurrentUser, svc=Depends(service)):
    return svc.save_lesson(user, course_id, body, lesson_id)


@router.put("/admin/courses/{course_id}")
def configure(course_id: str, body: CourseSettings, user: CurrentUser, svc=Depends(service)):
    return svc.configure(user, course_id, body)


@router.get("/courses/{course_id}")
def detail(course_id: str, user: CurrentUser, svc=Depends(service)):
    return svc.detail(user, course_id)


@router.post("/courses/{course_id}/redeem")
def redeem(course_id: str, body: CourseRedeem, user: CurrentUser, svc=Depends(service)):
    return svc.redeem(user, course_id, body)


@router.get("/courses/{course_id}/lessons/{lesson_id}")
def lesson(course_id: str, lesson_id: str, user: CurrentUser, svc=Depends(service)):
    return svc.lesson(user, course_id, lesson_id)


@router.put("/courses/{course_id}/lessons/{lesson_id}/progress")
def progress(course_id: str, lesson_id: str, body: LessonProgress, user: CurrentUser, svc=Depends(service)):
    return svc.progress(user, course_id, lesson_id, body.completed)


@router.get("/courses/{course_id}/lessons/{lesson_id}/video")
def video(course_id: str, lesson_id: str, user: CurrentUser, svc=Depends(service)):
    item = svc.lesson(user, course_id, lesson_id)
    if not item.get("video") or not MEDIA_PATH.is_file():
        fail("Video chưa sẵn sàng.", 404)
    return FileResponse(MEDIA_PATH, media_type="video/mp4", headers={"Cache-Control": "private, no-store"})
