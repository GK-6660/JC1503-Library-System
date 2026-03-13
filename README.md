## 📂 项目目录结构说明 (Project Structure)

为了确保开发不冲突，请各位成员严格按照以下结构存放代码：

### 1. `src/` - 源代码核心区
* **`main.py`**: 系统启动入口，负责调用各模块逻辑。
* **`models/`**: 业务逻辑对象定义。
    * `resource.py`: 抽象基类 `Resource` 以及 `Book`, `Magazine` 子类。(体现继承/多态)
    * `user.py`: `User` 类定义，包含个人借阅链表。
* **`structures/`**: 手动实现的底层数据结构 (严禁使用 Python 内置 list/dict 替代核心算法)。
    * `bst.py`: 二叉搜索树，用于按标题快速搜索图书。
    * `hash_table.py`: 哈希表，用于按 ID 快速索引用户。
    * `tree.py`: 通用树，用于学科分类层级管理。
    * `queue.py`: 队列，用于处理预约排队逻辑。
    * `linked_list.py`: 双向链表，用于管理用户的借阅记录。
    * `stack.py`: 栈，用于实现管理员操作的“撤销”功能。
* **`utils/`**: 工具模块。
    * `storage.py`: 负责 JSON 序列化与文件读写，实现数据持久化。
    * `exceptions.py`: 自定义异常类，增强系统鲁棒性。

### 2. `data/` - 数据存储区
* `library_data.json`: 运行生成的“数据库”，保存系统关闭前的所有状态。

### 3. `tests/` - 测试区
* 存放所有单元测试脚本，确保每个数据结构逻辑正确。

### 4. `docs/` - 文档与素材
* 存放 LaTeX 报告源码、类图图片 (UML) 及汇报视频素材。

---

# 🚀 JC1503-Library-System 团队工程化协作手册

大家好！我们的图书管理系统代码仓库已经建立。为了保证咱们后续开发高效推进，避免合并代码时出现“在你电脑上明明能跑，在我电脑上就报错”的玄学问题，本项目全面引入了现代化的 Python 工程流（uv + Ruff）以及严密的 Git 分支管理策略。

这套流程是正规软件工程开发的标准操作，请大家务必花三分钟仔细阅读，并严格照做！遇到任何报错，随时在群里截图找我（Team Leader）。

---

## 🛠️ 第一阶段：环境一键初始化（你的电脑仅需配置一次）

**A. 准备好开发武器**
请大家统一使用 VS Code（或 PyCharm）打开咱们已经克隆好的 JC1503-Library-System 文件夹。请确保你在编辑器左侧的文件树里，能直接看到 pyproject.toml 这个文件。

**B. 召唤内置终端（🔥 核心防坑操作）**
不要去外面开黑框框了！直接在编辑器里操作：
VS Code 用户请按快捷键 Ctrl + `（数字 1 左边那个键），或者点击顶部菜单栏的“终端 -> 新建终端”。
（注意看终端命令行前面的路径，末尾必须是 JC1503-Library-System！）

**C. 安装极速包管理器 uv**
在刚才打开的内置终端里，直接复制并回车运行：

`pip install uv`

（Windows 备选方案：如果上面这句报错，请运行 `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` ）

⚠️ 极易踩坑点：安装完成后，必须点击终端右上角的垃圾桶图标关掉当前终端，然后重新新建一个终端！输入 `uv --version`，看到输出版本号即代表系统已认识这个新工具。

**D. 一键生成虚拟环境**
确认你还在内置终端里，直接敲下这行魔法命令：

`uv sync`

系统会自动根据我的配置清单，在项目里秒建一个 .venv 虚拟环境并装好所有库。从此以后，严禁任何人私自用 pip install 瞎装东西！

**E. 让编辑器认领环境**
VS Code 用户请按 Ctrl+Shift+P (Mac 为 Cmd+Shift+P)，搜索 Python: Select Interpreter，选择路径带有 JC1503-Library-System/.venv 的那个 Python 解释器。选完后代码里的红色报错就会消失。

---

## 💻 第二阶段：日常开发与提交规范

**A. 绝对红线：禁止直推 main 分支**
咱们的 main 分支已开启保护。开发新功能前，必须创建并切换到自己的专属分支：
先同步主干代码：
`git checkout main`
`git pull origin main`

开辟你的新分支（例如 feat-zzj-bst）：
`git checkout -b feat-你的拼音-file_name`

**B. 写代码与“一键整容”（提交前必做）**
代码写完后，为了消除大家缩进、引号等格式差异，提交前必须在终端运行以下两条命令：

`uv run ruff format .`
`uv run ruff check .`

如果不运行这两步，代码推送到云端后会立刻触发自动化报错（飘红），你的代码将直接被拒绝合并！

**C. 优雅提交代码**
确认改动：
`git status`

暂存改动：
`git add .`

书写规范的提交信息：
`git commit -m "feat: 新增了用户登录的数据结构验证"`

**D. Rebase（变基）防冲突与推送（🔥 进阶核心）**
如果在你写代码期间，main 分支有了别人的新代码，你需要把自己的改动“移”到最新代码之上，保持历史记录是一条直线：
更新本地主干：
`git checkout main`
`git pull origin main`

切回你的分支：
`git checkout feat-你的拼音-file_name`

执行变基：
`git rebase main`

（如果遇到 Conflict 冲突，请在编辑器中保留正确的代码并删掉多余符号，然后运行 `git add .` 和 `git rebase --continue`）

推送至云端：
`git push origin feat-你的拼音-file_name`

**E. 提交 PR (Pull Request)**
在 GitHub 网页端点击 Compare & pull request，指定我进行 Code Review（代码审查）。审核通过后即可并入主干。

---
