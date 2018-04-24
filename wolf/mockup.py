from datetime import timedelta, date

from restfulpy.orm import DBSession
from restfulpy.cli import ProgressBar

from .models import Token, Cryptomodule


def insert(quantity=10, prefix=0):
    quantity = int(quantity)
    prefix = int(prefix)
    cryptomodule_ids = DBSession.query(Cryptomodule.id).all()
    expire_date = date.today() + timedelta(days=20000)
    with ProgressBar(quantity*2+1) as progress:
        for i in range(quantity):
            for (cryptomodule_id, ) in cryptomodule_ids:
                token = Token()
                token.name = f'{prefix:02}{i:010}{cryptomodule_id:02}'
                token.phone = int(f'989{i:09}')
                token.cryptomodule_id = cryptomodule_id
                token.initialize_seed()
                token.expire_date = expire_date
                token.is_active = True
                DBSession.add(token)
                DBSession.flush()
                progress.increment()
        DBSession.commit()
        progress.increment()

