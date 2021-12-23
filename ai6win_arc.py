# Class for packing and unpacking AI6WIN .arc archives.
# Before I hath implemented Silky Engine's arc. Now it is time for this one...
# These archives are quite far, yet they has some common traits.
# Namely, names obfusification and compression.

# Header.
## 4 bytes for number of entries.
## In each entry:
### 260 bytes for name (encrypted/obfusificated, see "decrypt_name".
### 4 bytes (<I) for LZSS compressed size.
### 4 bytes (<I) for uncompressed size.
### 4 bytes (<I) for data offset from the beginning of file.
## Next is data... Compressed by Silky's implementation of LZSS.

import os
import struct
import tempfile
from silky_arc import SilkyArc


class AI6WINArc(SilkyArc):  # Previously released tool came to be handy.
    # Some part of the class is from SilkyArcTool.
    name_encoding = "cp932"
    bytes_for_name = 260

    def __init__(self, arc: str, dir: str, verbose: bool = True, integrity_check: bool = False):
        """Parameters:
arc: name of the archive file,
dir: name of the directory,
verbose: False (no progress messages) or True (enable progress messages)."""
        super().__init__(arc, dir, verbose, integrity_check)
        # names
        # 0 -- padding, 1 -- name, 2 -- compressed in lzss size, 3 -- size after lzss decompression,
        # 4 -- offset from the beginning of file.

    # imported methods: unpack, pack, lzss_compress, lzss_decompress, read_header...
    # _unpack_files,

    # Unpacking methods.

    def _unpack_names(self) -> list:
        input_file = open(self._arc_name, 'rb')
        entry_count = self._read_header(input_file)
        array_name = []
        for entrer in range(entry_count):
            prms = []
            prms.append(None)  # Crutch to support imported function.

            name = self.decrypt_name(input_file.read(self.bytes_for_name))
            prms.append(name)
            for i in range(3):
                prms.append(struct.unpack('>I', input_file.read(4))[0])
            array_name.append(prms)

            # Header len is 4 + entry_count*(260+4*3)
        input_file.close()

        return array_name

    # Packing methods.

    def _pack_names_and_files(self) -> tuple:
        names = []
        sum = 4

        temp_file = tempfile.TemporaryFile(mode="w+b")

        for root, dirs, files in os.walk(self._dir_name):
            for filename in files:
                name_array = []

                rel_name = os.path.normpath(os.path.join(root, filename))
                end_name = rel_name
                if rel_name.startswith(root + os.sep):
                    end_name = rel_name[len(root + os.sep):]
                encrypted_name = self.encrypt_name(end_name)

                with open(rel_name, 'rb') as this_file:
                    this_bytes = this_file.read()
                encrypted_bytes = self.lzss_compress(this_bytes)

                temp_file.write(encrypted_bytes)

                name_array.append(None)  # Padding to support SilkyArc methods.
                name_array.append(encrypted_name)  # Filename (encrypted).
                name_array.append(len(encrypted_bytes))  # Filename (encrypted).
                name_array.append(len(this_bytes))  # Filename (encrypted).
                name_array.append(None)  # Offset from the start of file (currently unknown).

                names.append(name_array)

                sum += 272
                # 1 байт за размер имени, далее имя, далее три >I параметра.

                if self._verbose:
                    print("> File {0} successfully managed!/Файл {0} успешно обработан!".format(end_name))

        head_len = len(names)  # Not the header length, rather number of entries.

        for i in range(len(names)):
            names[i][4] = sum
            sum += names[i][2]
        if self._verbose:
            print(">>> File offsets successfully calculated!/Смещения файлов успешно подсчитаны!")

        return head_len, names, temp_file

    def _pack_files(self, head_len: int, temp_file: tempfile.TemporaryFile) -> None:
        new_archive = open(self._arc_name, 'wb')
        new_archive.write(struct.pack('I', head_len))

        for i in self._names:
            new_archive.write(i[1])
            for j in range(2, 5):
                new_archive.write(struct.pack('>I', i[j]))
        if self._verbose:
            print(">>> Archive header successfully created!/Заголовок архива успешно создан!")

        temp_file.seek(0)
        for i in self._names:
            new_bytes = temp_file.read(i[2])
            if self._integrity_check:
                try:
                    assert len(new_bytes) == i[2]
                except AssertionError:
                    print("!!! File {0} compressed size is incorrect!/Размер сжатого файла {0} некорректен!".format(
                        self.decrypt_name(i[1])))
            new_archive.write(new_bytes)
        if self._verbose:
            print(">>> Archive files data successfully packed!/Данные файлов архива успешно запакованы!")

        new_archive.close()
        temp_file.close()

    # Other technical methods.

    @staticmethod
    def decrypt_name(test: bytes) -> str:
        """Decrypt AI6WIN-encrypted header entry name."""
        test = test.rstrip(b'\x00')
        tester = b''
        k = 1
        for i in range(len(test) - 1, -1, -1):
            k += 1
            tester = struct.pack('B', test[i] - k) + tester
        name = tester.decode(SilkyArc.name_encoding)
        return name

    @staticmethod
    def encrypt_name(test: str) -> bytes:
        """Encrypt AI6WIN-encrypted header entry name."""
        text_array = test.encode(AI6WINArc.name_encoding)
        tester = b''
        k = 1
        for i in range(len(text_array) - 1, -1, -1):
            k += 1
            tester = struct.pack('B', text_array[i] + k) + tester
        check_len = len(tester)
        if check_len >= AI6WINArc.bytes_for_name:
            tester = tester[:AI6WINArc.bytes_for_name]
        else:
            tester += b'\x00' * (AI6WINArc.bytes_for_name - check_len)
        return tester
