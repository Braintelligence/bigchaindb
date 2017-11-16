import pytest


@pytest.mark.bdb
@pytest.mark.tendermint
def test_get_txids_filtered(signed_create_tx, signed_transfer_tx):
    from bigchaindb.backend import connect, query
    from bigchaindb.models import Transaction
    conn = connect()

    # create and insert two blocks, one for the create and one for the
    # transfer transaction
    conn.db.transactions.insert_one(signed_create_tx.to_dict())
    conn.db.transactions.insert_one(signed_transfer_tx.to_dict())

    asset_id = Transaction.get_asset_id([signed_create_tx, signed_transfer_tx])

    # Test get by just asset id
    txids = set(query.get_txids_filtered(conn, asset_id))
    assert txids == {signed_create_tx.id, signed_transfer_tx.id}

    # Test get by asset and CREATE
    txids = set(query.get_txids_filtered(conn, asset_id, Transaction.CREATE))
    assert txids == {signed_create_tx.id}

    # Test get by asset and TRANSFER
    txids = set(query.get_txids_filtered(conn, asset_id, Transaction.TRANSFER))
    assert txids == {signed_transfer_tx.id}
