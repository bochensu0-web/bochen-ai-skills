# 国内 OJ、算法竞赛与机试实战防坑指南

处理 PTA（拼题A）、洛谷、牛客网、蓝桥杯、CCF CSP、408/保研夏令营机试题目时按需读取本文件。

---

## 1. 国内常见平台规则与致命坑点

| 平台/考试 | 模式与环境特点 | 极易丢分陷阱 |
| --- | --- | --- |
| **PTA（拼题A / 团体程序设计天梯赛）** | ACM 模式；课程作业与期末上机高频平台 | **格式极严**：部分老题严格检查“行末不得有多余空格”、空集/全负特判（如最大子列和全负数时按题意输出 `0` 还是首尾元素必须细读题面！）；测试点常含 $N=1$、链表只有头节点或悬空地址 `-1`。 |
| **洛谷 / Codeforces** | ACM 模式；子任务（Subtask）捆绑或按点给分 | 多组测试 `T` 组数据下总和 $\sum n \le 2 \times 10^5$，若每组 `memset(vis, 0, sizeof vis)` 全量清空会直接 TLE（应按 `1..n` 局部清空）。 |
| **牛客网（笔试/机试常用）** | 兼有核心代码模式与 ACM 模式；真题多用 ACM 模式 | 字符串与整行读取混用时 `cin >> n` 后直接 `getline` 读到残留换行符；树/图输入未说明有向无向或根节点编号（`0` vs `1`）。 |
| **CCF CSP 认证** | 4 小时 5 题，无实时完整错误数据反馈（考场有提交次数但需自测） | **第 1–2 题稳拿 200 分**：重审题与 `long long`；**第 3 题大模拟/文本解析**：模块化拆函数，先写小解析器单测再拼装，不写 300 行巨型 `main`；**第 4–5 题**：必看表格里前 30%–50% 的特殊性质子任务（链、菊花图、小 $n$ 暴力 DP）抢部分分！ |
| **蓝桥杯（C++/Python 组）** | OI 赛制（赛时只过样例，赛后统一评测，**0 容错**！） | 赛时过了样例不等于对！必须关注编译器标准（部分环境不支持过新 C++20 语法）、`1LL` 乘法溢出、Python 递归深度与常数超时；关键题用暴力程序 + 随机数据生成器**对拍**验证。 |
| **学校期末卷手写代码** | 纸面人工阅卷，按关键逻辑块给步骤分 | 不用 `#define int long long` 或晦涩 lambda；写清结构体字段注释、空树/空表 `if (head == NULL) return ...` 边界判空、主循环注释，即使细节差一点也能拿 80% 步骤分。 |

---

## 2. ACM 模式 C++ / Python 稳健输入输出模板

### C++17 读写加速与多测安全骨架
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
using ll = long long;

void solve() {
    int n;
    if (!(cin >> n)) return;
    vector<ll> a(n); // 局部容器自动释放，避免多测残留与手动清空遗漏
    for (int i = 0; i < n; ++i) cin >> a[i];
    // PTA 行末无多余空格标准写法：
    for (int i = 0; i < n; ++i) {
        cout << a[i] << (i + 1 == n ? '\n' : ' ');
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 注意：开启 sync_with_stdio(false) 后严禁混用 scanf/printf/getchar！
    int T = 1;
    // cin >> T; // 多组数据时取消注释
    while (T--) solve();
    return 0;
}
```

### Python 大输入防 TLE/MLE 骨架
```python
import sys

# 递归深搜/树形 DP 必加（注意同时评估栈内存）：
sys.setrecursionlimit(200000)

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    nums = [int(next(it)) for _ in range(n)]
    sys.stdout.write(" ".join(map(str, nums)) + "\n")

if __name__ == "__main__":
    main()
```

---

## 3. 提交前 30 秒必查 6 问（WA / RE / TLE 自救）

1. **爆 `int` 了吗？** 前缀和、距离数组 `dist`、二分中点 `l + (r - l) / 2`、乘法 `(ll)a * b`、`1LL << k`（`1 << 31` 是 UB！）。
2. **数组开够了吗？** 无向图链式前向星边数是否开了 `2 * M + 5`？线段树空间是否开了 `4 * N`？离散化值域统计清了吗？
3. **边界输入崩了吗？** $n = 0$、$n = 1$、图不连通、全为负数、答案恰好为 0、起终点重合时输出什么？
4. **多测清空干净且不超时吗？** 优先使用局部 `vector`；全局邻接表或树状数组只清 `1..n` 范围。
5. **浮点数比较安全吗？** 避免直接 `==`，使用 `eps = 1e-9`；输出固定小数位用 `cout << fixed << setprecision(6)`。
6. **能拿多少保底分？** 机试还剩 20 分钟做不出正解时，果断写时间复杂度稳过的暴力/特殊性质分支拿满子任务分。
