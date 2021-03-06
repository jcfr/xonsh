"""Event tests"""
import inspect
import pytest
from xonsh.events import EventManager, Event, LoadEvent

@pytest.fixture
def events():
    return EventManager()

def test_event_calling(events):
    called = False

    @events.on_test
    def _(spam):
        nonlocal called
        called = spam

    events.on_test.fire("eggs")

    assert called == "eggs"

def test_event_returns(events):
    called = 0

    @events.on_test
    def on_test():
        nonlocal called
        called += 1
        return 1

    @events.on_test
    def second():
        nonlocal called
        called += 1
        return 2

    vals = events.on_test.fire()

    assert called == 2
    assert set(vals) == {1, 2}

def test_validator(events):
    called = None

    @events.on_test
    def first(n):
        nonlocal called
        called += 1
        return False

    @first.validator
    def v(n):
        return n == 'spam'

    @events.on_test
    def second(n):
        nonlocal called
        called += 1
        return False

    called = 0
    events.on_test.fire('egg')
    assert called == 1

    called = 0
    events.on_test.fire('spam')
    assert called == 2


def test_eventdoc(events):
    docstring = "Test event"
    events.doc('on_test', docstring)

    assert inspect.getdoc(events.on_test) == docstring


def test_transmogrify(events):
    docstring = "Test event"
    events.doc('on_test', docstring)

    @events.on_test
    def func():
        pass

    assert isinstance(events.on_test, Event)
    assert len(events.on_test) == 1
    assert inspect.getdoc(events.on_test) == docstring

    events.transmogrify('on_test', LoadEvent)

    assert isinstance(events.on_test, LoadEvent)
    assert len(events.on_test) == 1
    assert inspect.getdoc(events.on_test) == docstring

def test_transmogrify_by_string(events):
    docstring = "Test event"
    events.doc('on_test', docstring)

    @events.on_test
    def func():
        pass

    assert isinstance(events.on_test, Event)
    assert len(events.on_test) == 1
    assert inspect.getdoc(events.on_test) == docstring

    events.transmogrify('on_test', 'LoadEvent')

    assert isinstance(events.on_test, LoadEvent)
    assert len(events.on_test) == 1
    assert inspect.getdoc(events.on_test) == docstring

def test_typos(xonsh_builtins):
    for name, ev in vars(xonsh_builtins.events).items():
        if 'pytest' in name:
            continue
        assert inspect.getdoc(ev)
