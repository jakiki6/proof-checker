def normalize(statement, string=True, count=False):
    variable_counter = 0
    variables = {}

    def walk(part):
        nonlocal variable_counter, variables

        parts = [part[0]]

        for i in range(1, len(part)):
            if isinstance(part[i], str):
                if part[i] not in variables:
                    variables[part[i]] = "x" + str(variable_counter)
                    variable_counter += 1

                parts.append(variables[part[i]])
            else:
                parts.append(walk(part[i]))

        if string:
            return "(" + " ".join(parts) + ")"
        else:
            return parts

    if count:
        return walk(statement), variable_counter
    else:
        return walk(statement)


def check_logic(statement, variables):
    val = False
    if isinstance(statement, str):
        val = variables[statement]
    else:
        assert len(statement) > 0, "Empty statement"

        match statement[0]:
            case "eq":
                assert len(statement) == 3, "Eq takes 2 arguments"
                val = check_logic(statement[1], variables) == check_logic(
                    statement[2], variables)
            case "imp":
                assert len(statement) == 3, "Imp takes 2 arguments"
                val = (not check_logic(statement[1],
                                       variables)) or check_logic(
                                           statement[2], variables)
            case "or":
                assert len(statement) == 3, "Or takes 2 arguments"
                val = check_logic(statement[1], variables) or check_logic(
                    statement[2], variables)
            case "and":
                assert len(statement) == 3, "And takes 2 arguments"
                val = check_logic(statement[1], variables) and check_logic(
                    statement[2], variables)
            case "not":
                assert len(statement) == 2, "Or takes 1 argument"
                val = not check_logic(statement[1], variables)
            case _:
                raise ValueError(
                    f"Unknown logic statement {repr(statement[0])} in {statement}"
                )

    return val


def was_proven(statement, proven):
    return normalize(statement) in proven


def check(statements):
    proven = []

    for statement in statements:
        match statement[0]:
            case "stmt":
                to_prove = statement[1]

                for proof in statement[2:]:
                    match proof[0]:
                        case "truth":
                            assert len(
                                proof
                            ) == 2, "Truth table strategy only takes one argument"
                            normalized, variable_count = normalize(
                                proof[1], string=False, count=True)

                            is_true = True
                            for i in range(0, 1 << variable_count):
                                variables = {}
                                for j in range(0, variable_count):
                                    variables["x" + str(j)] = bool(i
                                                                   & (1 << j))

                                if not check_logic(normalized, variables):
                                    is_true = False
                                    break

                            if is_true:
                                proven.append(normalize(proof[1]))
                        case _:
                            raise ValueError(
                                f"Unknown proof strategy of {repr(proof[0])} in {proof}"
                            )

                if not was_proven(to_prove, proven):
                    return False, to_prove
            case _:
                raise ValueError(
                    f"Unknown root operation of {repr(statement[0])} in {statement}"
                )

    return True, None


__all__ = (check, )
