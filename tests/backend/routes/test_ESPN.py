import backend.routes.ESPN as ESPN

# only testing with mlb for now given games are played every day
def test_getTeamsPlayingToday():
    driver = ESPN.Util.connectDriver()
    result = ESPN.ESPN.getTeamsPlayingToday(driver, "MLB")
    driver.quit()

    assert (
        result
    ), "Result cannot be empty, check whether or not MLB teams are playing today"

    assert all(
        team in ESPN.ESPN.teams_dict['MLB'].values()
        for team in result
    )

def test_getRoster():
    driver = ESPN.Util.connectDriver()
    result = ESPN.ESPN.getRosters(driver, "MLB", ['phi'])
    driver.quit()

    assert (
        result
    ), "Roster cannot be empty"

    assert (
        'Bryce Harper' in result['phi'].keys()
    ), "Maybe Harper got traded or retired; ensure batters are still being read"

    assert (
        'Cristopher Sanchez' in result['phi'].keys()
    ), "Maybe Sanchez got traded or retired; ensure pitchers are still being read"

    assert (
        'John Doe Fake Player' not in result['phi'].keys()
    ), "A fake player should never be found in the player list"

def test_getStats():
    driver = ESPN.Util.connectDriver()
    roster = ESPN.ESPN.getRosters(driver, "MLB", ['phi'])
    result = ESPN.ESPN.getStats(driver, roster, 'MLB')
    driver.quit()

    assert (
        result
    ), "Roster cannot be empty"

    assert (
        'Bryce Harper' in result['phi'].keys()
    ), "This test is included to ensure next test fails due to getStats() not getRoster() issues"

    assert (
        'Cristopher Sanchez' in result['phi'].keys()
    ), "This test is included to ensure next test fails due to getStats(), not getRoster() issues"
        
    assert (
        19 == len(result['phi']['Bryce Harper'][0])
    ), "Batter storage should be a list of 19 values"

    assert (
        18 == len(result['phi']['Cristopher Sanchez'][0])
    ), "Pitcher storage should be a list of 18 values"