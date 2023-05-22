from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.router.hotel import get_hotels_by_location

# регистрация роута для HTML страниц
router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

# движок шаблонов
templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/hotels", response_class=HTMLResponse)
async def hotels(
        request: Request,
        hotels=Depends(get_hotels_by_location)
):
    """
    Хендлер для отрисовки html страницы списока отелей по заданным параметрам со свободными номерами.
    :param request: запрос
    :param hotels: локация гостиницы
    :return: html страница
    """
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )
