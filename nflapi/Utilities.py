import re

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