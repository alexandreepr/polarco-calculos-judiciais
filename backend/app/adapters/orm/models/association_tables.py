from sqlalchemy import ForeignKey, Integer, Table, Column

from base import Base

user_roles = Table(
    'user_roles', 
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
)

role_permissions = Table(
    'role_permissions', 
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE')),
)

user_permissions = Table(
    'user_permissions', 
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE')),
)

user_groups = Table(
    'user_groups', 
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE')),
)

group_roles = Table(
    'group_roles', 
    Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
)

##Review this implementation
company_user = Table(
    'company_user',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('company.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)