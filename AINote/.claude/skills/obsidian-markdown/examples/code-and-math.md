# Code and Math Examples

## Inline Code

Use `backticks` for inline code.

Use double backticks for ``code with ` backtick inside``.

Run `npm install` to install dependencies.

---

## Code Blocks

### Plain (No Highlighting)

```
This is a plain code block.
No syntax highlighting applied.
```

### JavaScript

```javascript
// Syntax-highlighted JavaScript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

const result = fibonacci(10);
console.log(`Fibonacci(10) = ${result}`);
```

### Python

```python
# Python with type hints
from typing import List, Optional

def binary_search(arr: List[int], target: int) -> Optional[int]:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None
```

### TypeScript

```typescript
interface User {
    id: number;
    name: string;
    email: string;
    roles: string[];
}

async function fetchUser(id: number): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
}
```

### Shell / Bash

```bash
#!/bin/bash
echo "Setting up environment..."
npm install
npm run build
docker compose up -d
echo "Done!"
```

### SQL

```sql
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.name
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC;
```

### JSON

```json
{
  "name": "obsidian-plugin",
  "version": "1.0.0",
  "description": "A sample plugin",
  "main": "main.js",
  "dependencies": {
    "obsidian": "^1.0.0"
  }
}
```

### CSS

```css
.callout[data-callout="custom"] {
    --callout-color: 100, 200, 150;
    --callout-icon: lucide-sparkles;
    border-radius: 8px;
    padding: 1rem;
}
```

### YAML

```yaml
title: My Note
date: 2024-01-15
tags:
  - project
  - active
aliases:
  - My Alias
```

---

## Nesting Code Blocks

Use more backticks for the outer fence:

````markdown
Here's how to show a code block in documentation:

```python
print("Hello, world!")
```
````

---

## Inline Math

Euler's identity: $e^{i\pi} + 1 = 0$

The quadratic formula: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$

Time complexity is $O(n \log n)$ for merge sort.

Probability: $P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$

---

## Block Math

### Basic Equation

$$
E = mc^2
$$

### Matrix

$$
\begin{bmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{bmatrix}
$$

### Determinant

$$
\begin{vmatrix}
a & b \\
c & d
\end{vmatrix} = ad - bc
$$

### Summation and Integration

$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$

$$
\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

### Attention Formula

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

### Multi-line Aligned Equations

$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{aligned}
$$

### Common LaTeX Symbols

| Symbol | LaTeX | Rendered |
|--------|-------|----------|
| Superscript | `$x^2$` | $x^2$ |
| Subscript | `$x_i$` | $x_i$ |
| Fraction | `$\frac{a}{b}$` | $\frac{a}{b}$ |
| Square root | `$\sqrt{x}$` | $\sqrt{x}$ |
| Cube root | `$\sqrt[3]{x}$` | $\sqrt[3]{x}$ |
| Summation | `$\sum_{i=1}^{n}$` | $\sum_{i=1}^{n}$ |
| Integral | `$\int_a^b$` | $\int_a^b$ |
| Greek | `$\alpha \beta \gamma$` | $\alpha \beta \gamma$ |
| Infinity | `$\infty$` | $\infty$ |
| Not equal | `$\neq$` | $\neq$ |
| Less/Greater | `$\leq \geq$` | $\leq \geq$ |
| Arrow | `$\rightarrow$` | $\rightarrow$ |
| Blackboard | `$\mathbb{R}$` | $\mathbb{R}$ |

---

## More Code Languages

### Rust

```rust
fn main() {
    let numbers: Vec<i32> = (1..=10).collect();
    let sum: i32 = numbers.iter().sum();
    println!("Sum: {}", sum);
}
```

### Go

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 5)
    for i := 1; i <= 5; i++ {
        ch <- i
    }
    close(ch)
    for v := range ch {
        fmt.Println(v)
    }
}
```

### Java

```java
public class BinarySearch {
    public static int search(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> nums = {3, 1, 4, 1, 5, 9};
    std::sort(nums.begin(), nums.end());
    for (int n : nums) std::cout << n << " ";
    return 0;
}
```

### Dockerfile

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### GraphQL

```graphql
type Query {
  user(id: ID!): User
  posts(authorId: ID): [Post!]!
}

type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}
```

### PowerShell

```powershell
$files = Get-ChildItem -Path . -Recurse -Filter *.md
$files | ForEach-Object {
    Write-Host "Processing: $($_.FullName)"
    $content = Get-Content $_.FullName
    # Process markdown content
}
```

### Markdown (for showing code blocks)

````markdown
```python
print("Hello")
```
````

---

## 来源

- [Obsidian Basic formatting syntax](https://obsidian.md/help/syntax) — Code blocks, inline code
- [Obsidian Advanced formatting syntax](https://obsidian.md/help/advanced-syntax) — Math blocks, LaTeX symbols
- [CommonMark Specification](https://spec.commonmark.org/) — Fenced code blocks, info strings
