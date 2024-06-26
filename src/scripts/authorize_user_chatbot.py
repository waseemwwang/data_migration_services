from datetime import UTC, datetime
from sqlalchemy import delete, update
from scripts.assist_abc import ScriptABC
from models.database import SessionManager
from models.chatbot import Project, ProjectOwner
from models.chatbot_auth import ChatbotUser, ChatbotUserProjectPermission
from models.enum import ChatbotUserRole
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from utils.logger import log


class AuthorizeUserChatbot(ScriptABC):

    def __init__(self) -> None:
        super().__init__("base")
        self.owners = None
        self.users = None
        self.project_owners = None

        self.add_users = []
        self.update_projects = []

    async def load_data(self, session: AsyncSession):
        # 1. 查询 project_owner项目负责人信息
        async with SessionManager("chatbot") as db:
            # 因为是短暂会话 with 推出后就无法继续使用会话查询 所以需要在这里直接查询出关联项
            # joinedload  急加载
            query = await db.execute(
                select(ProjectOwner).options(selectinload(ProjectOwner.project))
            )
            self.owners = query.scalars().all()

        # 2. 查询 chatbotuser信息
        query = await session.execute(
            select(ChatbotUser)
            .filter(ChatbotUser.deleted_at.is_(None))
            .options(selectinload(ChatbotUser.project))
        )
        self.users = query.scalars().all()

        # 3. 查询 chatbot user owner project信息
        query = await session.execute(
            select(ChatbotUserProjectPermission)
            .filter(ChatbotUserProjectPermission.deleted_at.is_(None))
            .filter(ChatbotUserProjectPermission.is_owner == True)
            .options(selectinload(ChatbotUserProjectPermission.user))
        )
        self.project_owners = query.scalars().all()

    async def process_data(self, session: AsyncSession):
        # 需要处理两件事情
        # 1. 判断项目负责人是否在chatbot_user表中
        # 2. 查询项目权限表 验证项目负责人是否正确 如果不正确需要修正
        users = {user.name: user for user in self.users}
        project_owners = {i.project_name: i.user for i in self.project_owners}

        for owner in self.owners:
            owner_name = owner.project_owner_name
            owner_user = users.get(owner_name)
            if owner_user is None:
                # 添加数据
                log.debug(f"owner name: {owner_name} not in Chatbot user tables")
                owner_user = ChatbotUser(
                    name=owner_name,
                    alias=owner.project_owner_alias,
                    email=owner.project_owner_email,
                    role=ChatbotUserRole.USER.value,
                )
                self.add_users.append(owner_user)
            for project in owner.project:
                old_project_owner = project_owners.get(project.project_name, None)
                if old_project_owner is not None:
                    if old_project_owner.name != owner_name:
                        # 需要替换信息
                        log.debug(
                            f"The project leader responsible for user {owner_name} is incorrect. \n"
                            + f"Revised from {old_project_owner.name} to {owner_name}",
                        )
                        self.update_projects.append(
                            {
                                "add": ChatbotUserProjectPermission(
                                    user_id=owner_user.id,
                                    project_id=project.project_id,
                                    project_name=project.project_name,
                                    is_owner=True,
                                ),
                                "delete": {
                                    "user_id": old_project_owner.id,
                                    "project": project,
                                },
                            }
                        )
                else:
                    # 添加数据 添加一条用户的负责项目数据
                    log.debug(
                        f"Add a responsible project {project.project_name} to user {owner.project_owner_name}",
                    )
                    new_permission = ChatbotUserProjectPermission(
                        user_id=owner_user.id,
                        project_id=project.project_id,
                        project_name=project.project_name,
                        is_owner=True,
                    )
                    owner_user.project.append(new_permission)

    async def update_data(self, session: AsyncSession):
        if len(self.add_users) > 0 or len(self.update_projects) > 0:
            if len(self.add_users) > 0:
                session.add_all(self.add_users)
            if len(self.update_projects):
                add_permission = []
                for udata in self.update_projects:
                    add_permission.append(udata["add"])
                    await session.execute(
                        update(ChatbotUserProjectPermission)
                        .where(
                            ChatbotUserProjectPermission.user_id
                            == udata["delete"]["user_id"],
                            ChatbotUserProjectPermission.is_owner == True,
                            ChatbotUserProjectPermission.project_id
                            == udata["delete"]["project"].project_id,
                            ChatbotUserProjectPermission.project_name
                            == udata["delete"]["project"].project_name,
                        )
                        .values(deleted_at=datetime.now(UTC))
                    )
        await session.commit()

    def as_result(self):
        log.debug(
            f"\n共有{len(self.owners)}个项目负责人 \n"
            + f"新增{len(self.add_users)}个用户 \n"
            + f"修正{len(self.update_projects)}个项目负责人信息",
        )

        return "Processing complete"
