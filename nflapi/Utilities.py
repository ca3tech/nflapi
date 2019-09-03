import re
import nflgame.statmap as sm

def parseYardLine(ydl : str, posteam : str) -> int:
    """Convert recorded yard line to a signed int

    Given a yard line like 'team_name yardline'.
    If the ydl value contains the given posteam
    then the resulting value will be yardline - 50,
    otherwise the value will be 50 - yardline.
    Basically this sets the 50 yard line to 0 and
    the return value is the distance from the 50
    yard line with the possession teams end resulting
    in a negative value. Thus the range is [-50, 50].

    Parameters
    ----------
    ydl : str
        The yard line value from the NFL source
    posteam : str
        The possession team

    Returns
    -------
    int
        The normalized yardline
    """
    if ydl == "50":
        yl = 0
    else:
        lty = ydl.split()
        assert len(lty) == 2, f"ydl value {ydl} not valid"
        if lty[0] == posteam:
            yl = int(lty[1]) - 50
        else:
            yl = 50 - int(lty[1])
    return yl

def getStatMetadata(statId : int) -> dict:
    """Get game play statistic metadata
    
    For a given statId value this will return a dict
    with the ID, category, description and long description.

    Parameters
    ----------
    statId : int
        The statId from the NFL API
    
    Returns
    -------
    dict
        See the description
    """
    d = {"stat_id": statId}
    for k, v in sm.idmap[statId].items():
        if not k in ["fields", "yds"]:
            if k == "long":
                fk = f"stat_desc_{k}"
            else:
                fk = f"stat_{k}"
            d[fk] = v
    return d