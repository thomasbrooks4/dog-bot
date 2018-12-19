import edjoin
from constants import SMS_HEADER, SMS_FOOTER
from twilio.twiml.messaging_response import MessagingResponse

def message_response(body):
    body_lower = body.lower()
    response = MessagingResponse()

    if 'search' in body_lower:
        if 'last' in body_lower:
            sms_body = 'Last search:\n\n' + edjoin.get_last_search()
        else:
            sms_body = edjoin.search()
    elif 'keyword' in body_lower:
        if 'get' in body_lower:
            sms_body = edjoin.keywords_string()
        elif 'add' in body_lower:
            split_body = body_lower.split(' ')

            if len(split_body) > (split_body.index('keyword') + 1):
                keyword = split_body[split_body.index('keyword') + 1].strip()

                keywords = edjoin.add_keyword(keyword)

                sms_body = 'Added keyword: ' + keyword + '\n\n' + edjoin.keywords_string()
            else:
                sms_body = 'Incorrect command. Command:\n"add keyword <keyword>"'
        elif 'remove' in body_lower:
            split_body = body_lower.split(' ')

            if len(split_body) > (split_body.index('keyword') + 1):
                keyword = split_body[split_body.index('keyword') + 1].strip()
                keywords = edjoin.remove_keyword(keyword)

                sms_body = 'Removed keyword: ' + keyword + '\n\n' + edjoin.keywords_string()
            else:
                sms_body = 'Incorrect command. Command:\n"remove keyword <keyword>"'
        elif 'default' in body_lower:
            keywords = edjoin.default_keywords()

            sms_body = 'Set keywords back to default.\n\n' + edjoin.keywords_string()
    elif 'blacklist' in body_lower:
        if 'get' in body_lower:
            sms_body = edjoin.blacklist_string()
        elif 'add' in body_lower:
            split_body = body_lower.split(' ')

            if len(split_body) > (split_body.index('blacklist') + 1):
                word = split_body[split_body.index('blacklist') + 1]
                blacklist = edjoin.add_to_blacklist(word)

                sms_body = 'Added word to blacklist: ' + word + '\n\nBlacklist:\n' + str(blacklist)
            else:
                sms_body = 'Incorrect command. Command:\n"add blacklist <word>"'
        elif 'remove' in body_lower:
            split_body = body_lower.split(' ')

            if len(split_body) > (split_body.index('blacklist') + 1):
                word = split_body[split_body.index('blacklist') + 1]
                blacklist = edjoin.remove_from_blacklist(word)

                sms_body = 'Removed word from blacklist: ' + word + '\n\nBlacklist:\n' + str(blacklist)
            else:
                sms_body = 'Incorrect command. Command:\n"remove blacklist <word>"'
        elif 'default' in body_lower:
            blacklist = edjoin.default_blacklist()

            sms_body = 'Set blacklist back to default.\n\nBlacklist:\n' + str(blacklist)
    elif 'commands' in body_lower:
        sms_body = 'Commands:\n'
        sms_body += '\n"search"'
        sms_body += '\n"last search"\n'
        sms_body += '\n"get keywords"'
        sms_body += '\n"add keyword <keyword>"'
        sms_body += '\n"remove keyword <keyword>"'
        sms_body += '\n"default keywords"\n'
        sms_body += '\n"get blacklist"'
        sms_body += '\n"add blacklist <word>"'
        sms_body += '\n"remove blacklist <word>"'
        sms_body += '\n"default blacklist"'
    else:
        sms_body = 'I\'m sorry. I could not recognize that command. Text "commands" to list some examples.'

    response.message(SMS_HEADER + sms_body + SMS_FOOTER)

    return response
