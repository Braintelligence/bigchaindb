import pytest

from bigchaindb.tendermint.lib import BigchainDB


@pytest.fixture(params=[None, BigchainDB])
def app(request):
    from bigchaindb.web import server
    app = server.create_app(debug=True, bigchaindb_factory=request.param)
    return app
