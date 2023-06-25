from dto.event import EventDTO
from shared.enums import PaymentStatus, EventStatus
from tgbot.shared.db.api import get_payment_by_user


async def create_event_text(event: EventDTO, state=None, **kwargs) -> str:
    text = ''
    text += f'Название: {event.name}\n'
    text += f'Описание: {event.description if event.description else ""}\n'
    text += f'Дата: {event.date if event.date else ""}\n'
    text += f'Кол-во участников: {event.max_participants if event.max_participants else 0}\n'
    text += f'Кол-во команд: {len(event.teams if event.teams else [])}\n'
    if 'status' in state:
        text += f'Статус: {event.status.value}\n'
    text += f'Сумма: {event.amount if event.amount else 0}\n\n'

    if 'name' in state:
        text += "Ведите название мероприятия"
    if 'description' in state:
        text += "Ведите описание мероприятия"
    if 'participants_limit' in state:
        text += "Укажите максимальное кол-во участников"
    if 'teams_count' in state:
        text += "Укажите кол-во команд"
    if 'payment_amount' in state:
        text += "Укажите стоимость мероприятия"
    if 'date' in state:
        text += "Укажите дату мероприятия в формате DD.MM.YYYY HH:mm"
    if 'links' in state:
        text += "Пригласительные ссылки:\n"
        for index, team in enumerate(event.teams):
            text += f"Команда {index + 1}: https://t.me/makeurmatch_bot?start={team.id}\n"
        text += "\n"
    if 'show_teams' in state:
        for index, team in enumerate(event.teams):
            text += f"Команда №{index + 1}:\n"
            if len(team.participants) > 0:
                for idx, player in enumerate(team.participants):
                    text += f"{idx + 1}. {player.full_name} @{player.id}"
                    if event.status == EventStatus.PAYMENT_WAIT:
                        payment = await get_payment_by_user(player.id, event.id)
                        print(payment)
                        if payment is not None and payment.status == PaymentStatus.PAID:
                            text += " (Оплачено)"

                    text += '\n'
            else:
                text += f"Участников ещё нет..."
            text += '\n\n'
    if 'payment' in state:
        if kwargs.get('payment_status') != PaymentStatus.PAID:
            text += f"Сумма к оплате: {kwargs.get('payment_amount')} тг.\n"
            text += f"Ваша ссылка на оплату:\n{kwargs.get('payment_link')}\n"
        else:
            text += f"Сумма к оплате: {kwargs.get('payment_amount')} тг. (Оплачено)\n"
    if 'cancel' in state:
        text += f"Мероприятие отменено\n"
    if 'refund' in state:
        text += f"Сумма к возврату: {kwargs.get('payment_amount')} тг.\n"
        text += f"Деньги вернуться к Вам в течении 3 рабочих дней\n"
    if 'canceled_by' in state:
        text += f"Участник отменивший оплату: {kwargs.get('canceled_by')}\n"

    return text
