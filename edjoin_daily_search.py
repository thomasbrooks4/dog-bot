import edjoin, sms
from private_constants import BRIANNA_NUMBER

sms.send(BRIANNA_NUMBER, edjoin.search())
