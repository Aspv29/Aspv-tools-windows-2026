; ASPV Tools Premium - NSIS Installer Configuration
; Custom installer settings and branding

!macro customHeader
  !system "echo ASPV Tools Premium Installer"
!macroend

!macro customInit
  ; Request admin privileges
  RequestExecutionLevel admin
!macroend

!macro customInstall
  ; Create desktop shortcut
  CreateShortCut "$DESKTOP\ASPV Tools Premium.lnk" "$INSTDIR\ASPV Tools Premium.exe"
  
  ; Create start menu folder
  CreateDirectory "$SMPROGRAMS\ASPV Tools Premium"
  CreateShortCut "$SMPROGRAMS\ASPV Tools Premium\ASPV Tools Premium.lnk" "$INSTDIR\ASPV Tools Premium.exe"
  CreateShortCut "$SMPROGRAMS\ASPV Tools Premium\Uninstall.lnk" "$INSTDIR\Uninstall ASPV Tools Premium.exe"
  
  ; Write registry keys for uninstaller
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ASPVToolsPremium" "DisplayName" "ASPV Tools Premium"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ASPVToolsPremium" "DisplayVersion" "3.0.0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ASPVToolsPremium" "Publisher" "ASPV Tools Team"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ASPVToolsPremium" "UninstallString" "$INSTDIR\Uninstall ASPV Tools Premium.exe"
!macroend

!macro customUnInstall
  ; Remove shortcuts
  Delete "$DESKTOP\ASPV Tools Premium.lnk"
  Delete "$SMPROGRAMS\ASPV Tools Premium\ASPV Tools Premium.lnk"
  Delete "$SMPROGRAMS\ASPV Tools Premium\Uninstall.lnk"
  RMDir "$SMPROGRAMS\ASPV Tools Premium"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ASPVToolsPremium"
!macroend
