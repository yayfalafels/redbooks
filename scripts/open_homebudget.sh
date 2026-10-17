#!/usr/bin/env bash
# Open the HomeBudget desktop app from WSL with the Java settings that fix its blank form fields.
# Same settings as the "HomeBudget (fixed UI).cmd" launcher on the Windows desktop.
set -euo pipefail

if [[ -e /mnt/c/users/admin/onedrive/documents/homebudgetdata/Logs/HomeBudget.log.0.lck ]]; then
  echo "HomeBudget is already running." >&2
  exit 1
fi

powershell.exe -NoProfile -Command "Start-Process -FilePath '.\runtime\bin\javaw.exe' \
  -WorkingDirectory 'C:\Program Files (x86)\HomeBudget' \
  -ArgumentList '-Djava.library.path=native','-Dsun.java2d.d3d=false','-Dsun.java2d.uiScale=1','-jar','HomeBudget.jar'"
echo "HomeBudget started."
