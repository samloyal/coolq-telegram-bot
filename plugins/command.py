from common import *
import re


def tg_command(bot, update):
    tg_group_id = update.message.chat_id  # telegram group id
    qq_group_id, _, forward_index = get_forward_index(tg_group_id=int(tg_group_id))
    if forward_index == -1:
        raise dispatcher.DispatcherHandlerStop()
    for command in global_vars.command_list:  # process all commands
        if update.message.text == command.command:
            command.handler(forward_index, tg_group_id, qq_group_id)
            raise dispatcher.DispatcherHandlerStop()


global_vars.dp.add_handler(MessageHandler(Filters.text, tg_command), 0)  # priority 0


@global_vars.qq_bot.listener((RcvdGroupMessage, ), 0)  # priority 0
def qq_drive_mode(message):
    qq_group_id = int(message.group)
    _, tg_group_id, forward_index = get_forward_index(qq_group_id=qq_group_id)
    if forward_index == -1:
        return True
    text = message.text  # get message text
    text, _ = re.subn('&amp;', '&', text)  # restore characters
    text, _ = re.subn('&#91;', '[', text)
    text, _ = re.subn('&#93;', ']', text)
    text, _ = re.subn('&#44;', ',', text)

    for command in global_vars.command_list:  # process all commands
        if text == command.command:
            command.handler(forward_index, tg_group_id, qq_group_id)
            return True

    return False