from ai6win_gui import AI6WINArcToolGUI

debug = False


def test(mode: str):
    from ai6win_arc import AI6WINArc
    """modes: unpack, pack,"""
    if mode == "unpack":
        test_arc = AI6WINArc("mes.arc", "mes", integrity_check=True)
        test_arc.unpack()
    elif mode == "pack":
        test_arc = AI6WINArc("mes.arc", "mes", integrity_check=True)
        test_arc.pack()


def main():
    AI6WINArcToolGUI()


if __name__ == '__main__':
    if debug:
        test("pack")
    else:
        main()
