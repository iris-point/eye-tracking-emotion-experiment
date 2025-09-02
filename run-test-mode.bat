@echo off
echo ╔════════════════════════════════════════════════════════╗
echo ║          测试模式 - TEST MODE                          ║
echo ║       情绪调节实验 - Emotion Regulation Experiment     ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 启动测试模式服务器... Starting test mode server...
echo.
echo 测试模式地址 Test Mode URL: http://localhost:8080/?test=true
echo.
echo 浏览器将在3秒后自动打开测试模式...
echo Browser will open test mode automatically in 3 seconds...
echo.
echo ────────────────────────────────────────────────────────
echo 测试模式将跳过实验，直接测试保存功能
echo Test mode will skip experiment and test save function
echo ────────────────────────────────────────────────────────
echo.
echo 按 Ctrl+C 停止服务器 (Press Ctrl+C to stop the server)
echo ────────────────────────────────────────────────────────
echo.

:: Start browser after 3 seconds with test mode
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8080/?test=true"

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