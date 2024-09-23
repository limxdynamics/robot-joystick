# robot-joystick

## 1. 下载运行

- 打开一个 Bash 终端。

- 下载 robot-joystick 代码：

  ```
  git clone --recurse https://github.com/limxdynamics/robot-joystick.git
  ```

- 安装运动控制开发库：

  - Linux x86_64 环境

    ```
    pip install robot-joystick/limxsdk/amd64/limxsdk-*-py3-none-any.whl
    ```

  - Linux aarch64 环境

    ```
    pip install robot-joystick/limxsdk/aarch64/limxsdk-*-py3-none-any.whl
    ```

- 运行 robot-joystick 仿真器：

  ```
  python robot-joystick/joystick.py
  ```

## 2. 效果展示
![](doc/joystick.png)
