from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.dialects.postgresql import UUID

from base import Base

user_roles = Table(
    'user_roles', 
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE')),
)

role_permissions = Table(
    'role_permissions', 
    Base.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE')),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id', ondelete='CASCADE')),
)

user_permissions = Table(
    'user_permissions', 
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id', ondelete='CASCADE')),
)

user_groups = Table(
    'user_groups', 
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')),
    Column('group_id', UUID(as_uuid=True), ForeignKey('groups.id', ondelete='CASCADE')),
)

group_roles = Table(
    'group_roles', 
    Base.metadata,
    Column('group_id', UUID(as_uuid=True), ForeignKey('groups.id', ondelete='CASCADE')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE')),
)

##Review this implementation
company_user = Table(
    'company_user',
    Base.metadata,
    Column('company_id', UUID(as_uuid=True), ForeignKey('company.id')),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
)