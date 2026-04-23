from fastapi import APIRouter, Body
from app.presentation.api.v1.dependencies.auth_dep import AuthorizationDep
from app.presentation.api.v1.dependencies import UserServiceDep
from app.presentation.api.v1.schemas.responses import AddedToContactResponse, UserContactsResponse

user_router = APIRouter(
    prefix="/user",
    tags=["User operation"]
)

@user_router.post("/add_contact", response_model=AddedToContactResponse)
async def add_user_to_contact(user: AuthorizationDep, user_service: UserServiceDep, contact_username: str = Body(embed=True)):
    await user_service.add_to_contact(user, contact_username)
    return AddedToContactResponse(succeed=True, detail="User added to contact")

@user_router.get("/get_contacts", response_model=UserContactsResponse)
async def get_contacts(user: AuthorizationDep, user_service: UserServiceDep):
    contacts = await user_service.get_contacts(user)
    return UserContactsResponse(succeed=True, detail="Spend list of user contacts", contacts=contacts)


