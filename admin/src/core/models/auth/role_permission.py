from src.core.database import Base, db
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.core.models.auth.user import User
    
class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Relaciones
    # Un rol puede tener múltiples asignaciones de permisos (One-to-Many con RolePermission)
    # Permite acceder a todas las asignaciones de permisos para este rol
    # Para obtener los permisos: [rp.permission for rp in role.role_permissions]
    role_permissions: Mapped[list["RolePermission"]] = relationship(back_populates="role")
    
    # Un rol puede ser asignado a múltiples usuarios (One-to-Many con User)
    # Permite acceder a todos los usuarios que tienen este rol asignado
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f'<Role - Name: {self.name}>'

    def get_permissions(self) -> list[str]:
        return [rp.permission.name for rp in self.role_permissions]
    
    def has_permission(self, permission_name: str) -> bool:
        return any(rp.permission.name == permission_name for rp in self.role_permissions)
    

class Permission(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Relaciones
    # Un permiso puede estar asignado a múltiples roles (One-to-Many con RolePermission)
    # Permite acceder a todas las asignaciones de roles que tienen este permiso
    role_permissions: Mapped[list["RolePermission"]] = relationship(back_populates="permission")

    def __repr__(self):
        return f'<Permission - Name: {self.name}>'
    

class RolePermission(Base):
    __tablename__ = 'role_permissions'
    
    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.id'),
        primary_key=True,
        nullable=False,
        comment="ID del rol al que se asigna el permiso"
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey('permissions.id'),
        primary_key=True,
        nullable=False,
        comment="ID del permiso que se asigna al rol"
    )

    # Relaciones
    # Many-to-One: Múltiples RolePermission pueden referenciar el mismo Role
    # Permite acceder al rol asociado con esta asignación de permiso
    role: Mapped["Role"] = relationship(back_populates="role_permissions")
    
    # Many-to-One: Múltiples RolePermission pueden referenciar el mismo Permission
    # Permite acceder al permiso asociado con esta asignación de rol
    permission: Mapped["Permission"] = relationship(back_populates="role_permissions")

    def __repr__(self):
        return f'<RolePermission - Role ID: {self.role_id} - Permission ID: {self.permission_id}>'
    