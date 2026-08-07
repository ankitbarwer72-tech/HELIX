# HELIX

HELIX is a lightweight, free Windows voice assistant for one laptop. It uses a small offline Vosk model for speech recognition and Windows' installed voices for speech output, so it does not need a GPU, subscription, cloud API key, or Microsoft Store publishing.

It recognises English, Hindi, and many Hinglish commands locally. Say `hello helix` / `हेलिक्स`, then speak naturally: `यूट्यूब खोलो`, `गूगल पर मौसम खोजो`, or `नोटपैड खोलो`.

Before using HELIX, run `dist\HELIX-ENROLL.exe` once and record three short samples of your own voice. HELIX checks this local voice profile for both the wake word and every command, and ignores other voices. This is a convenience feature, not a high-security authentication system: a high-quality recording or voice clone may be able to fool it.

## What it can do

- Open Brave, Google, and YouTube (Brave is always used for web links).
- Search Google: `search for Python tutorial`.
- Search YouTube: `search YouTube for lofi music`.
- Open any installed app shown in the Windows Start Menu: `open VS Code`, `open Steam`, or `open WhatsApp`.
- Open folders within Desktop, Documents, Downloads, Pictures, Music, and Videos: `open college project`.
- The launcher indexes those locations when HELIX starts. After installing an app or creating a new folder, say `refresh apps`.
- Accept a few Hinglish-style phrases such as `YouTube kholo`.

Say **"hello helix"**, wait for the reply, then say one command. Say **"shutdown"** to close it.

## Run from source

Install Python 3.11, 3.12, or 3.13 from [python.org](https://www.python.org/downloads/windows/) and check **Add Python to PATH** during setup. Then, in PowerShell at the project folder:

```powershell
python -m pip install -r requirements.txt
python -m src.main
```

## Create the EXE

```powershell
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1
```

The finished app will be at `dist\HELIX.exe`. Keep it in that folder after building; the packaged offline speech model is included in the EXE. The build automatically adds HELIX to your current Windows user's startup, so it opens every time you sign in after turning on the laptop.

To disable auto-start later:

```powershell
powershell -ExecutionPolicy Bypass -File .\remove_startup.ps1
```

## Notes

- Internet is only needed for Google/YouTube pages after they open in Brave. Voice recognition itself stays local.
- If Brave is installed somewhere unusual, update `possible_paths` in `src/actions/browser.py`.
- HELIX launches discovered Start Menu entries and personal folders, but never passes spoken words to PowerShell or Command Prompt. This prevents destructive or unintended commands from running.
