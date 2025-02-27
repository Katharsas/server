import pytest

from server.games import CustomGame, Game, LadderGame, VisibilityState
from server.players import PlayerState

pytestmark = pytest.mark.asyncio


async def test_initialization(game_service):
    assert len(game_service._dirty_games) == 0
    assert game_service.pop_dirty_games() == set()


async def test_create_game(players, game_service):
    players.hosting.state = PlayerState.IDLE
    game = game_service.create_game(
        visibility=VisibilityState.PUBLIC,
        game_mode="faf",
        host=players.hosting,
        name="Test",
        mapname="SCMP_007",
        password=None
    )
    assert game is not None
    assert game in game_service.pop_dirty_games()
    assert isinstance(game, CustomGame)

    game_service.remove_game(game)
    assert game not in game_service._games


async def test_all_games(players, game_service):
    game = game_service.create_game(
        visibility=VisibilityState.PUBLIC,
        game_mode="faf",
        host=players.hosting,
        name="Test",
        mapname="SCMP_007",
        password=None
    )
    assert game in game_service.pending_games
    assert isinstance(game, CustomGame)


async def test_create_game_ladder1v1(players, game_service):
    game = game_service.create_game(
        game_mode="ladder1v1",
        game_class=LadderGame,
        host=players.hosting,
        name="Test Ladder",
    )
    assert game is not None
    assert game in game_service.pop_dirty_games()
    assert isinstance(game, LadderGame)
    assert game.game_mode == "ladder1v1"


async def test_create_game_other_gamemode(players, game_service):
    game = game_service.create_game(
        visibility=VisibilityState.PUBLIC,
        game_mode="labwars",
        host=players.hosting,
        name="Test",
        mapname="SCMP_007",
        password=None
    )
    assert game is not None
    assert game in game_service.pop_dirty_games()
    assert isinstance(game, Game)
    assert game.game_mode == "labwars"
