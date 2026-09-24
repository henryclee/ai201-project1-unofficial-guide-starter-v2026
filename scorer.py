def judge(question, expects, answer, results):
    """
    Judge the answer based on the question, expected answers, and actual answer.
    Returns:
    - A boolean indicating whether the answer is correct or not.
    """
    for expectation in expects:
        if expectation.lower().strip() not in answer.lower():
            return False
    return True
