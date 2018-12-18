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
        sms_body += '\n"search"    -    Run search with current keywords/blacklist'
        sms_body += '\n"last search"    -    Return last search ran\n'
        sms_body += '\n"get keywords"    -    Return list of current keywords for search'
        sms_body += '\n"add keyword <keyword>"    -    Adds keyword to list of current keywords'
        sms_body += '\n"remove keyword <keyword>"    -    Removes keyword from list of current keywords'
        sms_body += '\n"default keywords"    -    Sets current keywords to default set of keywords\n'
        sms_body += '\n"get blacklist"    -    Return list of words blacklisted from job title or district name'
        sms_body += '\n"add blacklist <word>"    -    Adds word to current blacklist'
        sms_body += '\n"remove blacklist <word>"    -    Removes word from blacklist'
        sms_body += '\n"default blacklist"    -    Sets current blacklist to default blacklist'
    else:
        sms_body = 'I\'m sorry. I could not recognize that command. Text "commands" to list some examples.'

    response.message(SMS_HEADER + sms_body + SMS_FOOTER)

    return response
