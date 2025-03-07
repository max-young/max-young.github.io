---
layout: post
title: "useMemo or setState + useEffect"
date: 2024-07-17
categories: Frontend
tags:
  - React
---

Use `useMemo` like this:

```jsx
import React, { useState, useMemo } from 'react';

const ProductList = ({ products }) => {
  const [search, setSearch] = useState('');

  // Expensive filter function wrapped in useMemo
  const filteredProducts = useMemo(() => {
    console.log('Filtering products...');
    return products.filter((product) =>
      product.name.toLowerCase().includes(search.toLowerCase())
    );
  }, [products, search]); // Only recompute when products or search changes

  return (
    <div>
      <input
        type="text"
        placeholder="Search products"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <ul>
        {filteredProducts.map((product) => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
    </div>
  );
};

const App = () => {
  const products = Array.from({ length: 10000 }, (_, i) => ({
    id: i,
    name: `Product ${i}`,
  }));

  return <ProductList products={products} />;
};

export default App;
```

I have a question, why not use `setState` and `useEffect` like this:

```jsx
import React, { useState, useEffect } from 'react';

const ProductList = ({ products }) => {
  const [search, setSearch] = useState('');
  const [filteredProducts, setFilteredProducts] = useState([]);

  useEffect(() => {
    console.log('Filtering products...');
    setFilteredProducts(
      products.filter((product) =>
        product.name.toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [products, search]);

  return (
    <div>
      <input
        type="text"
        placeholder="Search products"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <ul>
        {filteredProducts.map((product) => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
    </div>
  );
};

const App = () => {
  const products = Array.from({ length: 10000 }, (_, i) => ({
    id: i,
    name: `Product ${i}`,
  }));

  return <ProductList products={products} />;
};

export default App;
```

The `useMemo` version is more efficient because it only recomputes the filtered products when the `products` or `search` state changes. The `setState` and `useEffect` version recomputes the filtered products on every render, which is unnecessary.

That's a great observation! Using `useEffect` with `setState` works fine in this case, but there are some subtle **differences** between this approach and using `useMemo`.

### 🔑 Differences
| Approach              | Pros                         | Cons                         |
|---------------------|-----------------------------|-----------------------------|
| `useEffect` + `setState` | Easier to understand, keeps filtered data in state | Can cause **extra re-renders** (due to state updates) |
| `useMemo`           | Avoids re-renders, **directly returns the memoized value** | More concise, but might look unfamiliar to some developers |

---

### How They Work Internally
1. **`useEffect` + `setState` Flow:**
   - When `search` or `products` changes, React triggers the `useEffect` hook.
   - Inside the effect, `setFilteredProducts` updates the state.
   - Updating state causes the component to **re-render**.

2. **`useMemo` Flow:**
   - When `search` or `products` changes, React **immediately computes** the filtered result.
   - The result is memoized and returned **without causing a re-render**.

---

### Performance Considerations
| Case                  | `useEffect` + `setState` | `useMemo` |
|---------------------|-----------------------------|----------|
| Large List + Frequent Typing | ❌ More re-renders | ✅ Fewer re-renders |
| Simple Calculations    | ✅ No visible difference | ✅ No visible difference |
| Complex Calculations   | ❌ Slightly slower        | ✅ Faster |

---

### When to Use Each?
| Use Case               | Recommended Approach |
|-----------------------|---------------------|
| Filtering small lists  | `useEffect` + `setState` (simpler code) |
| Filtering large lists  | `useMemo` (better performance) |
| Pure Computations      | `useMemo` |
| Side Effects (API calls, timers) | `useEffect` |

---

### Conclusion
If your component **doesn't need to store** the filtered list in state or trigger side effects, **`useMemo` is the better choice** because it avoids unnecessary re-renders and keeps the code cleaner.

If you're updating the filtered list in response to **external events** (like API calls or user interactions beyond filtering), then **`useEffect` makes more sense**.

Would you like a benchmark comparison between these two methods with performance metrics? 📊



