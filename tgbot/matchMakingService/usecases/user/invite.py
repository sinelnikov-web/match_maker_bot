from dto import UserDTO
from tgbot.shared.db.api import add_user_in_team, remove_user_from_team


async def accept_invite(user: UserDTO, team_id: str):
    await add_user_in_team(user.id, team_id)


async def leave_from_team(user: UserDTO, team_id: str):
    await remove_user_from_team(user.id, team_id)