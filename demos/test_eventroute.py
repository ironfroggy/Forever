from foreverdrive.base import EventRouter

class FakeEvent(object):
    type = "keyup"
    key = "somekey"

router = EventRouter()
L = []
router.listen(L.append, "keyup", "somekey")
router.route(FakeEvent())

assert L[0].key == "somekey"
