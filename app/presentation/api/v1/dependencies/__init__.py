from app.presentation.api.v1.dependencies.connection_dep import ConManagerDep
from app.presentation.api.v1.dependencies.session_dep import SessionDep, RedisDep
from app.presentation.api.v1.dependencies.repositories_deps import UserRepositoryDep, MessageRepoDep, ChatRepoDep
from app.presentation.api.v1.dependencies.cache_deps import TokenCacheDep
from app.presentation.api.v1.dependencies.services_deps import AuthServiceDep, UserServiceDep, JWTServiceDep, ChatServiceDep
from app.presentation.api.v1.dependencies.auth_dep import AuthorizationWsDep, AuthorizationDep