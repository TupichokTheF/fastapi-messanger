from app.presentation.api.v1.dependencies.session_dep import SessionDep, RedisDep
from app.presentation.api.v1.dependencies.repositories_deps import UserRepositoryDep, TokenRepositoryDep, MessageRepoDep
from app.presentation.api.v1.dependencies.services_deps import AuthServiceDep, UserServiceDep, JWTServiceDep, MessageServiceDep
from app.presentation.api.v1.dependencies.auth_dep import AuthorizationWsDep, AuthorizationDep
from app.presentation.api.v1.dependencies.connection_dep import ConManagerDep