const { app, BrowserWindow, screen } = require('electron');
let win;
function createWindow() {
    // 获取屏幕的工作区域（不包括任务栏等）
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;
    // 设置数字人窗口大小及位置（屏幕右下角）
    const windowWidth = 360;  // 你可以根据需要调整
    const windowHeight = 640; // 你可以根据需要调整
    win = new BrowserWindow({
        width: windowWidth,
        height: windowHeight,
        frame: false, // 设置为无边框窗口
        transparent: true, // 设置窗口背景透明（可选）
        alwaysOnTop: true, // 窗口始终置顶（可选）
        x: width - windowWidth,  // 屏幕右边缘
        y: height - windowHeight, // 屏幕下边缘
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        }
    });

    win.loadURL('http://127.0.0.1:11444/desktop.html');  // Flask 服务器地址

    // 允许鼠标穿透，但仍能与窗口内元素交互
    win.setIgnoreMouseEvents(true, { forward: true });

    // 强制最前 & 监听失焦
    win.setAlwaysOnTop(true, 'screen-saver');
    win.on('focus', () => {
        win.setIgnoreMouseEvents(false); // 允许点击交互
    });

    // 以下内容好像不是很必要， 反而影响
    // win.on('blur', () => {
    //     win.setIgnoreMouseEvents(true, { forward: true }); // 让鼠标穿透，  全部穿透， 就不能点元素了
    // });
    //   win.on('blur', () => {
    //       win.setIgnoreMouseEvents(true, { forward: true }); // 让鼠标穿透
    //       setTimeout(() => {
    //           win.setAlwaysOnTop(true, 'screen-saver');
    //           win.focus();
    //       }, 500);
    //   });

    // setInterval(() => {
    //     win.focus();
    // }, 1000);
}

app.whenReady().then(createWindow);

const { spawn } = require('child_process');

const flaskProcess = spawn('python', ['run.py']);  // 启动 Flask
flaskProcess.stdout.on('data', (data) => console.log(data.toString()));
