"""Tkinter GUI helpers for file selection and user feedback."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox


def select_file() -> str | None:
    """Open a file dialog and return the selected HTML file path.

    Returns:
        The selected file path, or ``None`` if the user cancelled.
    """
    root = tk.Tk()
    root.withdraw()

    filepath = filedialog.askopenfilename(
        title="Select Kindle Export File",
        filetypes=[("HTML files", "*.html")],
    )

    root.destroy()
    return filepath or None


def show_result(success: int, failure: int, total: int) -> None:
    """Show an informational dialog with import results."""
    root = tk.Tk()
    root.withdraw()

    if failure == 0:
        messagebox.showinfo(
            "Book2Notion",
            f"Import complete!\n{success}/{total} highlights imported successfully.",
        )
    else:
        messagebox.showwarning(
            "Book2Notion",
            f"Import finished with errors.\n"
            f"Success: {success}/{total}\n"
            f"Failed: {failure}/{total}",
        )

    root.destroy()


def show_error(message: str) -> None:
    """Show an error dialog."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Book2Notion - Error", message)
    root.destroy()
