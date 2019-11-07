# [LCP 3. 机器人大冒险](https://leetcode-cn.com/problems/programmable-robot/)

**难度:** 中等

力扣团队买了一个可编程机器人，机器人初始位置在原点 `(0, 0)` 。小伙伴事先给机器人输入一串指令 `command` ，机器人就会 **无限循环** 这条指令的步骤进行移动。指令有两种：
- U: 向y轴正方向移动一格
- R: 向x轴正方向移动一格。

不幸的是，在 xy 平面上还有一些障碍物，他们的坐标用 `obstacles` 表示。机器人一旦碰到障碍物就会被 **损毁** 。

给定终点坐标 `(x, y)` ，返回机器人能否 **完好** 地到达终点。如果能，返回 `true` ；否则返回 `false` 。

 **示例 1：** 

```
输入：command = "URR", obstacles = [], x = 3, y = 2
输出：true
解释：U(0, 1) -> R(1, 1) -> R(2, 1) -> U(2, 2) -> R(3, 2)。
```

 **示例 2：** 

```
输入：command = "URR", obstacles = [[2, 2]], x = 3, y = 2
输出：false
解释：机器人在到达终点前会碰到(2, 2)的障碍物。
```

 **示例 3：** 

```
输入：command = "URR", obstacles = [[4, 2]], x = 3, y = 2
输出：true
解释：到达终点后，再碰到障碍物也不影响返回结果。
```

 **限制：** 
- 2 <= command的长度 <= 1000
- command由U，R构成，且至少有一个U，至少有一个R
- 0 <= x <= 1e9, 0 <= y <= 1e9
- 0 <= obstacles的长度 <= 1000
- obstacles[i]不为原点或者终点

## Solution


**Language:** C++
```C++
class Solution {
   public:
    bool robot(string command, vector<vector<int>>& obstacles, int x, int y) {
        int dx = 0, dy = 0;
        unordered_map<int, int> t;
        t[0] = 1;
        for (int i = 0; i < command.size(); ++i) {
            if (command[i] == 'U')
                ++dy;
            else
                ++dx;
            t[1000 * dx + dy] = i + 2;
        }
        int _min = min(x / dx, y / dy);
        x -= _min * dx, y -= _min * dy;
        if (!t[1000 * x + y]) return false;
        int steps = _min * command.size() + t[1000 * x + y];
        for (auto d : obstacles) {
            _min = min(d[0] / dx, d[1] / dy);
            d[0] -= _min * dx, d[1] -= _min * dy;
            if (!t[1000 * d[0] + d[1]]) continue;
            if (t[1000 * d[0] + d[1]] + _min * command.size() < steps)
                return false;
        }
        return true;
    }
};
```

**Language:** Python3
```Python
class Solution:
    def robot(self, command: str, obstacles: List[List[int]], x: int,
              y: int) -> bool:
        dx = dy = 0
        t = {0: 0}
        for i, d in enumerate(command):
            if d == "U": dy += 1
            else: dx += 1
            t[1000 * dx + dy] = i + 1
        _min = min(x // dx, y // dy)
        x -= _min * dx
        y -= _min * dy
        if 1000 * x + y not in t: return False
        steps = _min * len(command) + t[1000 * x + y]
        for d in obstacles:
            _min = min(d[0] // dx, d[1] // dy)
            d[0] -= _min * dx
            d[1] -= _min * dy
            if 1000 * d[0] + d[1] not in t: continue
            if t[1000 * d[0] + d[1]] + _min * len(command) < steps:
                return False
        return True
```