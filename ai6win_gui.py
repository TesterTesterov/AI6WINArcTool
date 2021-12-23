# GUI for this tool. Nothing more, nothing less.

from tkinter.messagebox import showinfo, showwarning, showerror
from ai6win_arc import AI6WINArc
from gui import SilkyArcToolGUI  # Truly got in handy.


class AI6WINArcToolGUI(SilkyArcToolGUI):
    _strings_lib = {
        'eng': (
            "AI6WINArcTool by Tester",
            "English",
            "Русский",
            "...",
            "AI6WIN archive file (.arc):",
            "Resources directory:",  # 5
            "Filename choice",
            "Directory choice",
            "*.arc",
            "AI6WIN Archives",
            "*",  # 10
            "All files",
            "Unpack archive",
            "Pack archive",
            "Warning",
            "Archive name not stated.",  # 15
            "Directory name not stated.",
            "Error",
            "Help",
        ),
        'rus': (
            "AI6WINArcTool от Tester-а",
            "English",
            "Русский",
            "...",
            "Архивный файл AI6WIN (.arc):",
            "Директория с ресурсами:",  # 5
            "Выбор имени файла",
            "Выбор директории",
            "*.arc",
            "Архивы AI6WIN",
            "*",  # 10
            "Все файлы",
            "Распаковать архив",
            "Запаковать архив",
            "Предупреждение",
            "Имя архива не указано.",  # 15
            "Имя директории не указано.",
            "Ошибка",
            "Справка",
        )
    }

    program_help = {
        'eng': """
Dual languaged (rus+eng) GUI tool for packing and unpacking archives of AI6WIN engine. Very-very incomplete list of
games of the engine thou can see in the vndb. It is not the same arc as used in Silky Engine. For Silky Engine .arc
archives use SilkyArcTool instead!

>>> Usage.

1. Run the tool (main.py or .exe).
2. Print filename (with extension!!!) or choose it by clicking on button "...".
3. Print directory or choose it by clicking on button "...".
4. Print "0", if thou want to unpack, or "1", if thou want to pack.
5. Just wait until it done.
""",
        'rus': """
Двуязычное средство (рус+англ) для распаковки и запаковки архивов движка AI6WIN. Очень-преочень неполный список игр на
движке вы можете обозревать на vndb. Не стоит путать его с разновидностью .arc, используемой в Ai6WIN Для неё
используйте другое средство: SilkyArcTool!

>>> Использование.
1. Запустите пакет средств (main.py иль .exe).
2. Введите имя архива (с расширением!!!) или выберите его, нажав на кнопку "...".
3. Введите имя директории файлов или выберите его, нажав на кнопку "...".
4. Введите "0", коли распаковать желаете, али "1", коли запаковать желаете.
5. Ждите завершения.
"""
    }

    # Technical methods for packing and unpacking.

    def _unpack_this_archive(self, arc_name, dir_name) -> None:
        try:
            self.lock_activity()
            arc_archive = AI6WINArc(arc_name, dir_name, verbose=True, integrity_check=False)
            arc_archive.unpack()
        except Exception as e:
            showerror(self._strings_lib[self._language][17], str(e))
        finally:
            self.unlock_activity()

    def _pack_this_archive(self, arc_name, dir_name) -> None:
        try:
            self.lock_activity()
            arc_archive = AI6WINArc(arc_name, dir_name, verbose=True, integrity_check=False)
            arc_archive.pack()
        except Exception as e:
            showerror(self._strings_lib[self._language][17], str(e))
        finally:
            self.unlock_activity()
