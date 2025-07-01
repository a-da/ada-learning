"""Shell command wrapper"""
import subprocess
import sys
import threading
from typing import Sequence, IO


def _stream_output(stream: IO[str], tag: str, output_lines: list[tuple[str, str]]) -> None:
    for line in stream:
        print(f"{tag}: {line}", end='')
        output_lines.append((tag, line.strip()))


def bash(raw_command: Sequence[str | None] | str,
         show_but_not_execute: bool = False,
         exit_on_error_code: bool = True) -> tuple[int, Sequence[tuple[str, bytes]]]:
    """Run command in subprocess"""
    list_command: Sequence[str | None]

    if isinstance(raw_command, str):
        list_command = raw_command.split()
    else:
        list_command = raw_command

    command = tuple(i for i in list_command if i is not None)

    print(">", ' '.join(f'\\\n    {i}' if i.startswith('-') else i for i in command))

    if show_but_not_execute:
        return 0, [("", b"")]

    output_lines: Sequence[tuple[str, bytes]] = []

    with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
    ) as proc:
        threads = [
            threading.Thread(target=_stream_output, args=(proc.stdout, '🖨', output_lines)),
            threading.Thread(target=_stream_output, args=(proc.stderr, '❌', output_lines)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        proc.wait()  # Wait for the process to finish
        exit_code = proc.returncode
        if not exit_code:
            print('command succeeded ✅ ')
        else:
            print('command failed ⛔ ')

        if exit_on_error_code and exit_code:
            print(f"[HALT] with error code {exit_code}")
            sys.exit(exit_code)

        return exit_code, tuple(output_lines)


__all__ = ['bash']
