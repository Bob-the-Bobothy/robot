def clamp(n, minn, maxn):
    """Clamp a variable to a minimum and maximum value

    Args:
        n (_type_): input number
        minn (_type_): max value to clamp to
        maxn (_type_): minimum value to clamp to

    Returns:
        _type_: clamped value of input
    """    
    return max(min(maxn, n), minn)

def squareInput(input: float) -> float:
    """Function to square inputs from typically a control stick to smooth driving

    Args:
        input (float): usually a stick value, between -1 and 1

    Returns:
        float: the input squared regardless of negativity
    """    
    return input ** 2 if input > 0 else -(input ** 2)