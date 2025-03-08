# Live2D Desktop 桌面

## 功能描述

桌面版右下角摆一个Live2D， 播放语音，PPT同步翻页。

![cover](https://github.com/sndnyang/live2d-desktop/blob/master/images/live2d_desktop.png)

*注意事项：* PPT播放属于管理员权限， 所以要翻页的话，程序也要以管理员权限运行。 如果是WPS的播放就不需要。

技术上可实现把放映窗口从后台调上来，代码有找到，没集成。

## 使用说明

### 1. 安装依赖

#### Python
见：requirements.txt

```
pip install -r requirements.txt
```

JS库：bootstrap.bundle.min.js,  bootstrap.min.css,  cubism4.min.js,  jquery-3.1.1.min.js , live2d.min.js  live2dcubismcore.min.js,  pixi.min.js


#### Node.js

npm 安装 electron

```
export ELECTRON_MIRROR="https://npmmirror.com/mirrors/electron/"
npm install electron --save-dev       # jquery 就没安装成功， 这个electron成功了。
```

版本
```
node -v  # v20.13.1
npm -v   # 10.5.2
```


### 2. Live2D 形象

考虑到模型大小显然比纯文本代码文件大得多， 虽然实际放了两个模型也只12M， 自行下载及换形象（不一定会进一步完善“设置”功能）

模型来源：

- [live2d-TTS-LLM-GPT-SoVITS-Vtuber](https://github.com/v3ucn/live2d-TTS-LLM-GPT-SoVITS-Vtuber)
- [Live2D Sample Data(for Free)](https://www.live2d.com/en/learn/sample/)
- [Live2D Widget看板娘](https://github.com/stevenjoezhang/live2d-widget) 这里好像有不少Live2D 形象， 没看过怎么调用，好像不是cubism4.min.js

### 3. 内容

播放script1.txt文件里的内容

逐行播放， 每行播放完毕，相应PPT会翻一页。

翻页对应接口位置

```
run.py 106行
@app.route("/goclick", methods=["POST"])
def go_click():

desktop.html 208行
fetch('/goclick', { method: 'POST', });
```

### 4. 运行


Python 运行网页形式

```
python debug.py  # flask 可调试
python run.py    # 没考虑 gunicorn啥的
```

桌面版

```
npm start       # 请先管理员权限
```

Electron 打包成 exe， 没看。

## TODO

- [x] 单live2d形象
- [x] 单live2d形象 + Edge-tts 语音流
- [x] PPT控制
- [x] 无窗口、无背景处理（桌面版）
- []  大模型
- []  语音识别交互

## 参考

[live2d-TTS-LLM-GPT-SoVITS-Vtuber](https://github.com/v3ucn/live2d-TTS-LLM-GPT-SoVITS-Vtuber)

## 介绍

[AI power Education Group in CCNU(APEG-CCNU)](https://yangxlai.github.io/Group/)

<a href="https://yangxlai.github.io/Group/"><font color=red>A</font>I <font color=red>P</font>ower <font color=red>E</font>ducation <font color=red>G</font>roup in CCNU(<font color=red>APEG-CCNU</font>)</a>
