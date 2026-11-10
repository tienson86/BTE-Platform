from datetime import datetime, timezone
from applications.api.tests.test_membership import system
from applications.api.services.activity_service import ActivityService


def test_header_wallet_is_private_and_returns_only_current_owner_balance(system):
    client,service,store,headers=system
    activity=ActivityService(store)
    with activity.connect() as c:
        for owner,amount in [('u-existing',3),('u-testadmin',41)]:
            c.execute('INSERT INTO linh_ledger VALUES(?,?,?,?,?,?,?)',('seed:'+owner,owner,amount,'test','Test',None,datetime.now(timezone.utc).isoformat()))
    path='/api/v1/membership/wallet-balance'
    assert client.get(path).status_code==401
    response=client.get(path,headers=headers('existing'))
    assert response.status_code==200 and response.json()=={'balance':3}
    assert response.headers['cache-control']=='private, no-store'
    assert client.get(path+'?owner=u-testadmin',headers=headers('existing')).json()=={'balance':3}
    assert client.get(path,headers=headers('testadmin')).json()=={'balance':41}


def test_zero_negative_and_locked_wallets(system):
    client,service,store,headers=system
    path='/api/v1/membership/wallet-balance'
    auth=headers('existing')
    assert client.get(path,headers=auth).json()=={'balance':0}
    with ActivityService(store).connect() as c:
        c.execute("INSERT INTO linh_ledger VALUES('refund','u-existing',-7,'test','Test',NULL,?)",(datetime.now(timezone.utc).isoformat(),))
    assert client.get(path,headers=auth).json()=={'balance':-7}
    store.get_by_username('existing').is_active=False
    assert client.get(path,headers=auth).status_code==401
