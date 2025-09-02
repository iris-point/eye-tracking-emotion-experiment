@echo off
echo ╔════════════════════════════════════════════════════════╗
echo ║       情绪调节实验 - Emotion Regulation Experiment     ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 启动实验服务器... Starting experiment server...
echo.
echo 服务器地址 Server URL: http://localhost:8080
echo.
echo 浏览器将在3秒后自动打开...
echo Browser will open automatically in 3 seconds...
echo.
echo ────────────────────────────────────────────────────────
echo 按 Ctrl+C 停止服务器 (Press Ctrl+C to stop the server)
echo ────────────────────────────────────────────────────────
echo.

:: Start browser after 3 seconds
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8080"

:: Start the server
node server.js 8080

:: If node fails, provide help
if errorlevel 1 (
    echo.
    echo ╔════════════════════════════════════════════════════════╗
    echo ║                         错误 ERROR                      ║
    echo ╚════════════════════════════════════════════════════════╝
    echo.
    echo 未找到 Node.js - Node.js not found
    echo.
    echo 请安装 Node.js - Please install Node.js:
    echo https://nodejs.org/
    echo.
    pause
)