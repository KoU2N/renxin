# 授课机器人项目
## 启动日期
2018.11.28
## 成员
Professor Ren，gy，lz，zz，lje
## 关于源码
- 环境
    - python3.6.7
    - GUI库是pyqt5
- 目前master是脱离机器人环境,大家本地搭建一下帮完善一下requirements.txt
- 后续计划俩个branch
    - master -> 机器人环境代码(windows)
    - test -> 脱离机器人环境，方便在自己电脑上开发
## 工作安排
- [ ] **任务2019年2月25日**
    - [ ] lz
        - [ ] 唇形匹配方案
        - [ ] gTTS生成语音替换为百度男声，可行方案./python_test/baidu_tts.py
    - [ ] zz
        - [ ] ppt播放前进后退功能
    - [ ] lje
        - [ ] 一席ppt处理,文本:./play/一席.txt,ppt: A1服务器/任先生/Yixi
    - [ ] gy
        - [ ] 基于HMM的个性化TTS
- [ ] **任务进度总览**
    - [x] 主程序
        - [x] 各模块集成
        - [x] pyqt5多线程
    - [x] ppt预处理
        - [x] 读取ppt备注
        - [x] 调用gTTS生成语音
        - [x] 控制脚本生成
    - [x] 语音生成
        - [ ] 个性化语音合成
    - [x] 控制脚本
        - [ ] 唇形匹配
        - [x] 脚本生成
    - [x] ppt播放模块
        - [x] 调用office ppt全屏播放
        - [x] 播放暂停
        - [x] 进度条 
    - [x] 事件监测
        - [x] openpose集成
        - [x] 举手动作识别  
    - [ ] QA模块  