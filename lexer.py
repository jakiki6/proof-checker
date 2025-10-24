class LexError(ValueError):

    def __init__(self, msg, t):
        super().__init__(self)
        self.msg = msg
        self.index = len(t)


def lex_inner(t):
    t = t.lstrip()

    while len(t) > 0 and t[0] == "%":
        while len(t) > 0 and t[0] != "\n":
            t = t[1:]

        t = t.lstrip()

    if len(t) == 0:
        raise LexError("Premature end of text", t)

    if t[0] == "(":
        elements = []
        t = t[1:].lstrip()

        while True:
            if len(t) == 0:
                raise LexError("Premature end of text", t)

            if t[0] == ")":
                break

            element, t = lex_inner(t)
            elements.append(element)
            t = t.lstrip()

        return elements, t[1:]
    else:
        name = ""
        while len(t) > 0 and t[0] not in " ()":
            name += t[0]
            t = t[1:]

        return name, t


def lex(t):
    if len(t.strip()) == 0:
        return iter([])

    t = t.strip()
    ot = t
    while len(t):
        try:
            element, t = lex_inner(t)
            t = t.lstrip()
            yield element
        except LexError as err:
            index = len(ot) - err.index
            raise ValueError(
                f"{err.msg}: at index {index} ({repr(ot[max(index - 10, 0):index])} <- here)"
            )


__all__ = (lex, )
