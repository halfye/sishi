@echo off
if exist ./Scripts/mitmdump.exe (
	set local=./Scripts/mitmdump.exe
)else set local=mitmdump.exe
for /f "tokens=3 delims= " %%i in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable') do (
	if "%%i" equ "0x0" (
		reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f >nul
		reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "127.0.0.1:8080" /f>nul
		reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /d "127.0.0.1" /f>nul
		echo �����ô���
		echo ���ڵȴ���������
		start  /b  %local% -s 44.py 
	)
	if "%%i" equ "0x1" (
		reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f >nul
		echo ��ֹͣ����
		taskkill /f /im "mitmdump.exe"
		echo ��ֹͣ���
		pause
	)
)
echo �л��ɹ�!
