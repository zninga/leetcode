# 穷举n位二进制数

例如，穷举 `n=3` 的所有二进制数为: `[000,001,010,011,100,101,110,111]`.

对于每个位置，取值可为 `0|1`，所有可能情况一共有 `1<<n` 种，每种情况的取值与 `[0,(1<<n)-1]` 相对应.

## 循环遍历`[0,(1<<n)-1]`转为二进制输出

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    string bin(int n, int N) {
        string s(N, '0');
        for (int i = 0; n; ++i, n /= 2) {
            if (n % 2) s[i] = '1';
        }
        return string(s.rbegin(), s.rend());
    }

    vector<string> search(int n) {
        vector<string> v;
        int N = 1 << n;
        for (int i = 0; i < N; ++i) {
            v.push_back(bin(i, n));
        }
        return v;
    }
};

int main() {
    vector<string> v = Solution().search(3);
    for (auto s : v) {
        cout << s << '\n';
    }

    return 0;
}
```

## 回溯每个位置选择置为 '0' 或 '1'

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    vector<string> v;
    void fun(int k, int n, string s) {
        if (k == n) {
            v.push_back(s);
        } else {
            s[k] = '0';
            fun(k + 1, n, s);
            s[k] = '1';
            fun(k + 1, n, s);
        }
    }
    vector<string> search(int n) {
        fun(0, n, string(n, '0'));
        return v;
    }
};

int main() {
    vector<string> v = Solution().search(3);
    for (auto s : v) {
        cout << s << '\n';
    }

    return 0;
}
```





