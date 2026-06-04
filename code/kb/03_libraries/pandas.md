# 10 Minutes to pandas

Source: https://pandas.pydata.org/docs/user_guide/10min.html

# 10 minutes to pandas

This is a short introduction to pandas, geared mainly for new users. You can see more complex recipes in the [Cookbook](cookbook.html#cookbook).

Customarily, we import as follows:

```python
In [1]: import numpy as np

In [2]: import pandas as pd
```

## Basic data structures in pandas

pandas provides two types of classes for handling data:

1. **Series**: a one-dimensional labeled array holding data of any type such as integers, strings, Python objects etc.

2. **DataFrame**: a two-dimensional data structure that holds data like a two-dimension array or a table with rows and columns.

## Object creation

Creating a Series by passing a list of values, letting pandas create a default RangeIndex.

```python
In [3]: s = pd.Series([1, 3, 5, np.nan, 6, 8])

In [4]: s
Out[4]: 
0    1.0
1    3.0
2    5.0
3    NaN
4    6.0
5    8.0
dtype: float64
```

Creating a DataFrame by passing a NumPy array with a datetime index using `date_range()` and labeled columns:

```python
In [5]: dates = pd.date_range("20130101", periods=6)

In [6]: dates
Out[6]: 
DatetimeIndex(['2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04',
               '2013-01-05', '2013-01-06'],
              dtype='datetime64[us]', freq='D')

In [7]: df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

In [8]: df
Out[8]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-05 -0.424972  0.567020  0.276232 -1.087401
2013-01-06 -0.673690  0.113648 -1.478427  0.524988
```

Creating a DataFrame by passing a dictionary of objects where the keys are the column labels and the values are the column values.

```python
In [9]: df2 = pd.DataFrame(
   ...:    {
   ...:        "A": 1.0,
   ...:        "B": pd.Timestamp("20130102"),
   ...:        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
   ...:        "D": np.array([3] * 4, dtype="int32"),
   ...:        "E": pd.Categorical(["test", "train", "test", "train"]),
   ...:        "F": "foo",
   ...:    }
   ...: )
   ...

In [10]: df2
Out[10]: 
     A          B    C  D      E    F
0  1.0 2013-01-02  1.0  3   test  foo
1  1.0 2013-01-02  1.0  3  train  foo
2  1.0 2013-01-02  1.0  3   test  foo
3  1.0 2013-01-02  1.0  3  train  foo
```

The columns of the resulting DataFrame have different dtypes:

```python
In [11]: df2.dtypes
Out[11]: 
A           float64
B    datetime64[us]
C           float32
D             int32
E          category
F               str
dtype: object
```

If you're using IPython, tab completion for column names (as well as public attributes) is automatically enabled. Here's a subset of the attributes that will be completed:

```python
In [12]: df2.<TAB>  # noqa: E225, E999
df2.A                  df2.bool
df2.abs                df2.boxplot
df2.add                df2.C
df2.add_prefix         df2.clip
df2.add_suffix         df2.columns
df2.align              df2.copy
df2.all                df2.count
df2.any                df2.combine
df2.append             df2.D
df2.apply              df2.describe
df2.B                  df2.duplicated
df2.diff
```

As you can see, the columns `A`, `B`, `C`, and `D` are automatically tab completed. `E` and `F` are there as well; the rest of the attributes have been truncated for brevity.

## Viewing data

Use `DataFrame.head()` and `DataFrame.tail()` to view the top and bottom rows of the frame respectively:

```python
In [13]: df.head()
Out[13]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-05 -0.424972  0.567020  0.276232 -1.087401

In [14]: df.tail(3)
Out[14]: 
                   A         B         C         D
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-05 -0.424972  0.567020  0.276232 -1.087401
2013-01-06 -0.673690  0.113648 -1.478427  0.524988
```

Display the `DataFrame.index` or `DataFrame.columns`:

```python
In [15]: df.index
Out[15]: 
DatetimeIndex(['2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04',
               '2013-01-05', '2013-01-06'],
              dtype='datetime64[us]', freq='D')

In [16]: df.columns
Out[16]: Index(['A', 'B', 'C', 'D'], dtype='str')
```

Return a NumPy representation of the underlying data with `DataFrame.to_numpy()` without the index or column labels:

```python
In [17]: df.to_numpy()
Out[17]: 
array([[ 0.4691, -0.2829, -1.5091, -1.1356],
       [ 1.2121, -0.1732,  0.1192, -1.0442],
       [-0.8618, -2.1046, -0.4949,  1.0718],
       [ 0.7216, -0.7068, -1.0396,  0.2719],
       [-0.425 ,  0.567 ,  0.2762, -1.0874],
       [-0.6737,  0.1136, -1.4784,  0.525 ]])
```

**Note**: NumPy arrays have one dtype for the entire array while pandas DataFrames have one dtype per column. When you call `DataFrame.to_numpy()`, pandas will find the NumPy dtype that can hold all of the dtypes in the DataFrame. If the common data type is `object`, `DataFrame.to_numpy()` will require copying data.

```python
In [18]: df2.dtypes
Out[18]: 
A           float64
B    datetime64[us]
C           float32
D             int32
E          category
F               str
dtype: object

In [19]: df2.to_numpy()
Out[19]: 
array([[1.0, Timestamp('2013-01-02 00:00:00'), 1.0, 3, 'test', 'foo'],
       [1.0, Timestamp('2013-01-02 00:00:00'), 1.0, 3, 'train', 'foo'],
       [1.0, Timestamp('2013-01-02 00:00:00'), 1.0, 3, 'test', 'foo'],
       [1.0, Timestamp('2013-01-02 00:00:00'), 1.0, 3, 'train', 'foo']],
      dtype=object)
```

`describe()` shows a quick statistic summary of your data:

```python
In [20]: df.describe()
Out[20]: 
              A         B         C         D
count  6.000000  6.000000  6.000000  6.000000
mean   0.073711 -0.431125 -0.687758 -0.233103
std    0.843157  0.922818  0.779887  0.973118
min   -0.861849 -2.104569 -1.509059 -1.135632
25%   -0.611510 -0.600794 -1.368714 -1.076610
50%    0.022070 -0.228039 -0.767252 -0.386188
75%    0.658444  0.041933 -0.034326  0.461706
max    1.212112  0.567020  0.276232  1.071804
```

Transposing your data:

```python
In [21]: df.T
Out[21]: 
   2013-01-01  2013-01-02  2013-01-03  2013-01-04  2013-01-05  2013-01-06
A    0.469112    1.212112   -0.861849    0.721555   -0.424972   -0.673690
B   -0.282863   -0.173215   -2.104569   -0.706771    0.567020    0.113648
C   -1.509059    0.119209   -0.494929   -1.039575    0.276232   -1.478427
D   -1.135632   -1.044236    1.071804    0.271860   -1.087401    0.524988
```

`DataFrame.sort_index()` sorts by an axis:

```python
In [22]: df.sort_index(axis=1, ascending=False)
Out[22]: 
                   D         C         B         A
2013-01-01 -1.135632 -1.509059 -0.282863  0.469112
2013-01-02 -1.044236  0.119209 -0.173215  1.212112
2013-01-03  1.071804 -0.494929 -2.104569 -0.861849
2013-01-04  0.271860 -1.039575 -0.706771  0.721555
2013-01-05 -1.087401  0.276232  0.567020 -0.424972
2013-01-06  0.524988 -1.478427  0.113648 -0.673690
```

`DataFrame.sort_values()` sorts by values:

```python
In [23]: df.sort_values(by="B")
Out[23]: 
                   A         B         C         D
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-06 -0.673690  0.113648 -1.478427  0.524988
2013-01-05 -0.424972  0.567020  0.276232 -1.087401
```

## Selection

**Note**: While standard Python / NumPy expressions for selecting and setting are intuitive and come in handy for interactive work, for production code, we recommend the optimized pandas data access methods, `DataFrame.at()`, `DataFrame.iat()`, `DataFrame.loc()` and `DataFrame.iloc()`.

See the indexing documentation [Indexing and Selecting Data](indexing.html#indexing) and [MultiIndex / Advanced Indexing](advanced.html#advanced).

### Getitem (`[]`)

For a DataFrame, passing a single label selects a column and yields a Series:

```python
In [24]: df["A"]
Out[24]: 
2013-01-01    0.469112
2013-01-02    1.212112
2013-01-03   -0.861849
2013-01-04    0.721555
2013-01-05   -0.424972
2013-01-06   -0.673690
Freq: D, Name: A, dtype: float64
```

If the label only contains letters, numbers, and underscores, you can alternatively use the column name attribute:

```python
In [25]: df.A
Out[25]: 
2013-01-01    0.469112
2013-01-02    1.212112
2013-01-03   -0.861849
2013-01-04    0.721555
2013-01-05   -0.424972
2013-01-06   -0.673690
Freq: D, Name: A, dtype: float64
```

Passing a list of column labels selects multiple columns, which can be useful for getting a subset/rearranging:

```python
In [26]: df[["B", "A"]]
Out[26]: 
                   B         A
2013-01-01 -0.282863  0.469112
2013-01-02 -0.173215  1.212112
2013-01-03 -2.104569 -0.861849
2013-01-04 -0.706771  0.721555
2013-01-05  0.567020 -0.424972
2013-01-06  0.113648 -0.673690
```

For a DataFrame, passing a slice `:` selects matching rows:

```python
In [27]: df[0:3]
Out[27]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804

In [28]: df["20130102":"20130104"]
Out[28]: 
                   A         B         C         D
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
```

### Selection by label

See more in [Selection by Label](indexing.html#indexing-label) using `DataFrame.loc()` or `DataFrame.at()`.

Selecting a row matching a label:

```python
In [29]: df.loc[dates[0]]
Out[29]: 
A    0.469112
B   -0.282863
C   -1.509059
D   -1.135632
Name: 2013-01-01 00:00:00, dtype: float64
```

Selecting all rows (`:`) with a select column labels:

```python
In [30]: df.loc[:, ["A", "B"]]
Out[30]: 
                   A         B
2013-01-01  0.469112 -0.282863
2013-01-02  1.212112 -0.173215
2013-01-03 -0.861849 -2.104569
2013-01-04  0.721555 -0.706771
2013-01-05 -0.424972  0.567020
2013-01-06 -0.673690  0.113648
```

For label slicing, both endpoints are _included_:

```python
In [31]: df.loc["20130102":"20130104", ["A", "B"]]
Out[31]: 
                   A         B
2013-01-02  1.212112 -0.173215
2013-01-03 -0.861849 -2.104569
2013-01-04  0.721555 -0.706771
```

Selecting a single row and column label returns a scalar:

```python
In [32]: df.loc[dates[0], "A"]
Out[32]: np.float64(0.4691122999071863)
```

For getting fast access to a scalar (equivalent to the prior method):

```python
In [33]: df.at[dates[0], "A"]
Out[33]: np.float64(0.4691122999071863)
```

### Selection by position

See more in [Selection by Position](indexing.html#indexing-integer) using `DataFrame.iloc()` or `DataFrame.iat()`.

Select via the position of the passed integers:

```python
In [34]: df.iloc[3]
Out[34]: 
A    0.721555
B   -0.706771
C   -1.039575
D    0.271860
Name: 2013-01-04 00:00:00, dtype: float64
```

Integer slices acts similar to NumPy/Python:

```python
In [35]: df.iloc[3:5, 0:2]
Out[35]: 
                   A         B
2013-01-04  0.721555 -0.706771
2013-01-05 -0.424972  0.567020
```

Lists of integer position locations:

```python
In [36]: df.iloc[[1, 2, 4], [0, 2]]
Out[36]: 
                   A         C
2013-01-02  1.212112  0.119209
2013-01-03 -0.861849 -0.494929
2013-01-05 -0.424972  0.276232
```

For slicing rows explicitly:

```python
In [37]: df.iloc[1:3, :]
Out[37]: 
                   A         B         C         D
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
```

For slicing columns explicitly:

```python
In [38]: df.iloc[:, 1:3]
Out[38]: 
                   B         C
2013-01-01 -0.282863 -1.509059
2013-01-02 -0.173215  0.119209
2013-01-03 -2.104569 -0.494929
2013-01-04 -0.706771 -1.039575
2013-01-05  0.567020  0.276232
2013-01-06  0.113648 -1.478427
```

For getting a value explicitly:

```python
In [39]: df.iloc[1, 1]
Out[39]: np.float64(-0.17321464905330858)
```

For getting fast access to a scalar (equivalent to the prior method):

```python
In [40]: df.iat[1, 1]
Out[40]: np.float64(-0.17321464905330858)
```

### Boolean indexing

Select rows where `df.A` is greater than `0`.

```python
In [41]: df[df["A"] > 0]
Out[41]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
```

Selecting values from a DataFrame where a boolean condition is met:

```python
In [42]: df[df > 0]
Out[42]: 
                   A         B         C         D
2013-01-01  0.469112       NaN       NaN       NaN
2013-01-02  1.212112       NaN  0.119209       NaN
2013-01-03       NaN       NaN       NaN  1.071804
2013-01-04  0.721555       NaN       NaN  0.271860
2013-01-05       NaN  0.567020  0.276232       NaN
2013-01-06       NaN  0.113648       NaN  0.524988
```

Using `isin()` method for filtering:

```python
In [43]: df2 = df.copy()

In [44]: df2["E"] = ["one", "one", "two", "three", "four", "three"]

In [45]: df2
Out[45]: 
                   A         B         C         D      E
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632    one
2013-01-02  1.212112 -0.173215  0.119209 -1.044236    one
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804    two
2013-01-04  0.721555 -0.706771 -1.039575  0.271860  three
2013-01-05 -0.424972  0.567020  0.276232 -1.087401   four
2013-01-06 -0.673690  0.113648 -1.478427  0.524988  three

In [46]: df2[df2["E"].isin(["two", "four"])]
Out[46]: 
                   A         B         C         D     E
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804   two
2013-01-05 -0.424972  0.567020  0.276232 -1.087401  four
```

### Setting

Setting a new column automatically aligns the data by the indexes:

```python
In [47]: s1 = pd.Series(
   ....:   [1, 2, 3, 4, 5, 6],
   ....:   index=pd.date_range("20130102", periods=6))
   ....

In [48]: s1
Out[48]: 
2013-01-02    1
2013-01-03    2
2013-01-04    3
2013-01-05    4
2013-01-06    5
2013-01-07    6
Freq: D, dtype: int64

In [49]: df["F"] = s1
```

Setting values by label:

```python
In [50]: df.at[dates[0], "A"] = 0
```

Setting values by position:

```python
In [51]: df.iat[0, 1] = 0
```

Setting by assigning with a NumPy array:

```python
In [52]: df.loc[:, "D"] = np.array([5] * len(df))
```

The result of the prior setting operations:

```python
In [53]: df
Out[53]: 
                   A         B         C    D    F
2013-01-01  0.000000  0.000000 -1.509059  5.0  NaN
2013-01-02  1.212112 -0.173215  0.119209  5.0  1.0
2013-01-03 -0.861849 -2.104569 -0.494929  5.0  2.0
2013-01-04  0.721555 -0.706771 -1.039575  5.0  3.0
2013-01-05 -0.424972  0.567020  0.276232  5.0  4.0
2013-01-06 -0.673690  0.113648 -1.478427  5.0  5.0
```

A `where` operation with setting:

```python
In [54]: df2 = df.copy()

In [55]: df2[df2 > 0] = -df2

In [56]: df2
Out[56]: 
                   A         B         C    D    F
2013-01-01  0.000000  0.000000 -1.509059 -5.0  NaN
2013-01-02 -1.212112 -0.173215 -0.119209 -5.0 -1.0
2013-01-03 -0.861849 -2.104569 -0.494929 -5.0 -2.0
2013-01-04 -0.721555 -0.706771 -1.039575 -5.0 -3.0
2013-01-05 -0.424972 -0.567020 -0.276232 -5.0 -4.0
2013-01-06 -0.673690 -0.113648 -1.478427 -5.0 -5.0
```

## Missing data

For NumPy data types, `np.nan` represents missing data. It is by default not included in computations. See the [Missing Data section](missing_data.html#missing-data).

Reindexing allows you to change/add/delete the index on a specified axis. This returns a copy of the data:

```python
In [57]: df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ["E"])

In [58]: df1.loc[dates[0] : dates[1], "E"] = 1

In [59]: df1
Out[59]: 
                   A         B         C    D    F    E
2013-01-01  0.000000  0.000000 -1.509059  5.0  NaN  1.0
2013-01-02  1.212112 -0.173215  0.119209  5.0  1.0  1.0
2013-01-03 -0.861849 -2.104569 -0.494929  5.0  2.0  NaN
2013-01-04  0.721555 -0.706771 -1.039575  5.0  3.0  NaN
```

`DataFrame.dropna()` drops any rows that have missing data:

```python
In [60]: df1.dropna(how="any")
Out[60]: 
                   A         B         C    D    F    E
2013-01-02  1.212112 -0.173215  0.119209  5.0  1.0  1.0
```

`DataFrame.fillna()` fills missing data:

```python
In [61]: df1.fillna(value=5)
Out[61]: 
                   A         B         C    D    F    E
2013-01-01  0.000000  0.000000 -1.509059  5.0  5.0  1.0
2013-01-02  1.212112 -0.173215  0.119209  5.0  1.0  1.0
2013-01-03 -0.861849 -2.104569 -0.494929  5.0  2.0  5.0
2013-01-04  0.721555 -0.706771 -1.039575  5.0  3.0  5.0
```

`isna()` gets the boolean mask where values are `nan`:

```python
In [62]: pd.isna(df1)
Out[62]: 
                A      B      C      D      F      E
2013-01-01  False  False  False  False   True  False
2013-01-02  False  False  False  False  False  False
2013-01-03  False  False  False  False  False   True
2013-01-04  False  False  False  False  False   True
```

## Operations

See the [Basic section on Binary Ops](basics.html#basics-binop).

### Stats

Operations in general _exclude_ missing data.

Calculate the mean value for each column:

```python
In [63]: df.mean()
Out[63]: 
A   -0.004474
B   -0.383981
C   -0.687758
D    5.000000
F    3.000000
dtype: float64
```

Calculate the mean value for each row:

```python
In [64]: df.mean(axis=1)
Out[64]: 
2013-01-01    0.872735
2013-01-02    1.431621
2013-01-03    0.707731
2013-01-04    1.395042
2013-01-05    1.883656
2013-01-06    1.592306
Freq: D, dtype: float64
```

Operating with another Series or DataFrame with a different index or column will align the result with the union of the index or column labels. In addition, pandas automatically broadcasts along the specified dimension and will fill unaligned labels with `np.nan`.

```python
In [65]: s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)

In [66]: s
Out[66]: 
2013-01-01    NaN
2013-01-02    NaN
2013-01-03    1.0
2013-01-04    3.0
2013-01-05    5.0
2013-01-06    NaN
Freq: D, dtype: float64

In [67]: df.sub(s, axis="index")
Out[67]: 
                   A         B         C    D    F
2013-01-01       NaN       NaN       NaN  NaN  NaN
2013-01-02       NaN       NaN       NaN  NaN  NaN
2013-01-03 -1.861849 -3.104569 -1.494929  4.0  1.0
2013-01-04 -2.278445 -3.706771 -4.039575  2.0  0.0
2013-01-05 -5.424972 -4.432980 -4.723768  0.0 -1.0
2013-01-06       NaN       NaN       NaN  NaN  NaN
```

### User defined functions

`DataFrame.agg()` and `DataFrame.transform()` applies a user defined function that reduces or broadcasts its result respectively.

```python
In [68]: df.agg(lambda x: np.mean(x) * 5.6)
Out[68]: 
A    -0.025054
B    -2.150294
C    -3.851445
D    28.000000
F    16.800000
dtype: float64

In [69]: df.transform(lambda x: x * 101.2)
Out[69]: 
                     A           B           C      D      F
2013-01-01    0.000000    0.000000 -152.716721  506.0    NaN
2013-01-02  122.665737  -17.529322   12.063922  506.0  101.2
2013-01-03  -87.219115 -212.982405  -50.086843  506.0  202.4
2013-01-04   73.021382  -71.525239 -105.204988  506.0  303.6
2013-01-05  -43.007200   57.382459   27.954680  506.0  404.8
2013-01-06  -68.177398   11.501219 -149.616767  506.0  506.0
```

### Value Counts

See more at [Histogramming and Discretization](basics.html#basics-discretization).

```python
In [70]: s = pd.Series(np.random.randint(0, 7, size=10))

In [71]: s
Out[71]: 
0    4
1    2
2    1
3    2
4    6
5    4
6    4
7    6
8    4
9    4
dtype: int64

In [72]: s.value_counts()
Out[72]: 
4    5
2    2
6    2
1    1
Name: count, dtype: int64
```

### String Methods

Series is equipped with a set of string processing methods in the `str` attribute that make it easy to operate on each element of the array, as in the code snippet below. See more at [Vectorized String Methods](text.html#text-string-methods).

```python
In [73]: s = pd.Series(["A", "B", "C", "Aaba", "Baca", np.nan, "CABA", "dog", "cat"])

In [74]: s.str.lower()
Out[74]: 
0       a
1       b
2       c
3    aaba
4    baca
5     NaN
6    caba
7     dog
8     cat
dtype: str
```

## Merge

### Concat

pandas provides various facilities for easily combining together Series and DataFrame objects with various kinds of set logic for the indexes and relational algebra functionality in the case of join / merge-type operations.

See the [Merging section](merging.html#merging).

Concatenating pandas objects together row-wise with `concat()`:

```python
In [75]: df = pd.DataFrame(np.random.randn(10, 4))

In [76]: df
Out[76]: 
          0         1         2         3
0 -0.548702  1.467327 -1.015962 -0.483075
1  1.637550 -1.217659 -0.291519 -1.745505
2 -0.263952  0.991460 -0.919069  0.266046
3 -0.709661  1.669052  1.037882 -1.705775
4 -0.919854 -0.042379  1.247642 -0.009920
5  0.290213  0.495767  0.362949  1.548106
6 -1.131345 -0.089329  0.337863 -0.945867
7 -0.932132  1.956030  0.017587 -0.016692
8 -0.575247  0.254161 -1.143704  0.215897
9  1.193555 -0.077118 -0.408530 -0.862495

# break it into pieces
In [77]: pieces = [df[:3], df[3:7], df[7:]]

In [78]: pd.concat(pieces)
Out[78]: 
          0         1         2         3
0 -0.548702  1.467327 -1.015962 -0.483075
1  1.637550 -1.217659 -0.291519 -1.745505
2 -0.263952  0.991460 -0.919069  0.266046
3 -0.709661  1.669052  1.037882 -1.705775
4 -0.919854 -0.042379  1.247642 -0.009920
5  0.290213  0.495767  0.362949  1.548106
6 -1.131345 -0.089329  0.337863 -0.945867
7 -0.932132  1.956030  0.017587 -0.016692
8 -0.575247  0.254161 -1.143704  0.215897
9  1.193555 -0.077118 -0.408530 -0.862495
```

**Note**: Adding a column to a DataFrame is relatively fast. However, adding a row requires a copy, and may be expensive. We recommend passing a pre-built list of records to the DataFrame constructor instead of building a DataFrame by iteratively appending records to it.

### Join

`merge()` enables SQL style join types along specific columns. See the [Database style joining](merging.html#merging-join) section.

```python
In [79]: left = pd.DataFrame({"key": ["foo", "foo"], "lval": [1, 2]})

In [80]: right = pd.DataFrame({"key": ["foo", "foo"], "rval": [4, 5]})

In [81]: left
Out[81]: 
   key  lval
0  foo     1
1  foo     2

In [82]: right
Out[82]: 
   key  rval
0  foo     4
1  foo     5

In [83]: pd.merge(left, right, on="key")
Out[83]: 
   key  lval  rval
0  foo     1     4
1  foo     1     5
2  foo     2     4
3  foo     2     5
```

`merge()` on unique keys:

```python
In [84]: left = pd.DataFrame({"key": ["foo", "bar"], "lval": [1, 2]})

In [85]: right = pd.DataFrame({"key": ["foo", "bar"], "rval": [4, 5]})

In [86]: left
Out[86]: 
   key  lval
0  foo     1
1  bar     2

In [87]: right
Out[87]: 
   key  rval
0  foo     4
1  bar     5

In [88]: pd.merge(left, right, on="key")
Out[88]: 
   key  lval  rval
0  foo     1     4
1  bar     2     5
```

## Grouping

By "group by" we are referring to a process involving one or more of the following steps:

- **Splitting** the data into groups based on some criteria
- **Applying** a function to each group independently
- **Combining** the results into a data structure

See the [Grouping section](groupby.html#groupby).

```python
In [89]: df = pd.DataFrame(
   ....:    {
   ....:        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
   ....:        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
   ....:        "C": np.random.randn(8),
   ....:        "D": np.random.randn(8),
   ....:    }
   ....: )
   ....

In [90]: df
Out[90]: 
     A      B         C         D
0  foo    one  1.346061 -1.577585
1  bar    one  1.511763  0.396823
2  foo    two  1.627081 -0.105381
3  bar  three -0.990582 -0.532532
4  foo    two -0.441652  1.453749
5  bar    two  1.211526  1.208843
6  foo    one  0.268520 -0.080952
7  foo  three  0.024580 -0.264610
```

Grouping by a column label, selecting column labels, and then applying the `DataFrameGroupBy.sum()` function to the resulting groups:

```python
In [91]: df.groupby("A")[["C", "D"]].sum()
Out[91]: 
            C         D
A                      
bar  1.732707  1.073134
foo  2.824590 -0.574779
```

Grouping by multiple columns label forms MultiIndex.

```python
In [92]: df.groupby(["A", "B"]).sum()
Out[92]: 
                  C         D
A   B                        
bar one    1.511763  0.396823
    three -0.990582 -0.532532
    two    1.211526  1.208843
foo one    1.614581 -1.658537
    three  0.024580 -0.264610
    two    1.185429  1.348368
```

## Reshaping

See the sections on [Hierarchical Indexing](advanced.html#advanced-hierarchical) and [Reshaping](reshaping.html#reshaping-stacking).

### Stack

```python
In [93]: arrays = [
   ....:   ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
   ....:   ["one", "two", "one", "two", "one", "two", "one", "two"],
   ....: ]
   ....

In [94]: index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])

In [95]: df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=["A", "B"])

In [96]: df2 = df[:4]

In [97]: df2
Out[97]: 
                     A         B
first second                    
bar   one    -0.727965 -0.589346
      two     0.339969 -0.693205
baz   one    -0.339355  0.593616
      two     0.884345  1.591431
```

The `stack()` method "compresses" a level in the DataFrame's columns:

```python
In [98]: stacked = df2.stack()

In [99]: stacked
Out[99]: 
first  second   
bar    one     A   -0.727965
               B   -0.589346
       two     A    0.339969
               B   -0.693205
baz    one     A   -0.339355
               B    0.593616
       two     A    0.884345
               B    1.591431
dtype: float64
```

With a "stacked" DataFrame or Series (having a MultiIndex as the `index`), the inverse operation of `stack()` is `unstack()`, which by default unstacks the **last level**:

```python
In [100]: stacked.unstack()
Out[100]: 
                     A         B
first second                    
bar   one    -0.727965 -0.589346
      two     0.339969 -0.693205
baz   one    -0.339355  0.593616
      two     0.884345  1.591431

In [101]: stacked.unstack(1)
Out[101]: 
second        one       two
first                      
bar   A -0.727965  0.339969
      B -0.589346 -0.693205
baz   A -0.339355  0.884345
      B  0.593616  1.591431

In [102]: stacked.unstack(0)
Out[102]: 
first          bar       baz
second                      
one    A -0.727965 -0.339355
       B -0.589346  0.593616
two    A  0.339969  0.884345
       B -0.693205  1.591431
```

### Pivot tables

See the section on [Pivot Tables](reshaping.html#reshaping-pivot).

```python
In [103]: df = pd.DataFrame(
   .....:    {
   .....:        "A": ["one", "one", "two", "three"] * 3,
   .....:        "B": ["A", "B", "C"] * 4,
   .....:        "C": ["foo", "foo", "foo", "bar", "bar", "bar"] * 2,
   .....:        "D": np.random.randn(12),
   .....:        "E": np.random.randn(12),
   .....:    }
   .....: )
   ....

In [104]: df
Out[104]: 
        A  B    C         D         E
0     one  A  foo -1.202872  0.047609
1     one  B  foo -1.814470 -0.136473
2     two  C  foo  1.018601 -0.561757
3   three  A  bar -0.595447 -1.623033
4     one  B  bar  1.395433  0.029399
5     one  C  bar -0.392670 -0.542108
6     two  A  foo  0.007207  0.282696
7   three  B  foo  1.928123 -0.087302
8     one  C  foo -0.055224 -1.575170
9     one  A  bar  2.395985  1.771208
10    two  B  bar  1.552825  0.816482
11  three  C  bar  0.166599  1.100230
```

`pivot_table()` pivots a DataFrame specifying the `values`, `index` and `columns`

```python
In [105]: pd.pivot_table(df, values="D", index=["A", "B"], columns=["C"])
Out[105]: 
C             bar       foo
A     B                    
one   A  2.395985 -1.202872
      B  1.395433 -1.814470
      C -0.392670 -0.055224
three A -0.595447       NaN
      B       NaN  1.928123
      C  0.166599       NaN
two   A       NaN  0.007207
      B  1.552825       NaN
      C       NaN  1.018601
```

## Time series

pandas has simple, powerful, and efficient functionality for performing resampling operations during frequency conversion (e.g., converting secondly data into 5-minutely data). This is extremely common in, but not limited to, financial applications. See the [Time Series section](timeseries.html#timeseries).

```python
In [106]: rng = pd.date_range("1/1/2012", periods=100, freq="s")

In [107]: ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)

In [108]: ts.resample("5Min").sum()
Out[108]: 
2012-01-01    24182
Freq: 5min, dtype: int64
```

`Series.tz_localize()` localizes a time series to a time zone:

```python
In [109]: rng = pd.date_range("3/6/2012 00:00", periods=5, freq="D")

In [110]: ts = pd.Series(np.random.randn(len(rng)), rng)

In [111]: ts
Out[111]: 
2012-03-06    1.857704
2012-03-07   -1.193545
2012-03-08    0.677510
2012-03-09   -0.153931
2012-03-10    0.520091
Freq: D, dtype: float64

In [112]: ts_utc = ts.tz_localize("UTC")

In [113]: ts_utc
Out[113]: 
2012-03-06 00:00:00+00:00    1.857704
2012-03-07 00:00:00+00:00   -1.193545
2012-03-08 00:00:00+00:00    0.677510
2012-03-09 00:00:00+00:00   -0.153931
2012-03-10 00:00:00+00:00    0.520091
Freq: D, dtype: float64
```

`Series.tz_convert()` converts a timezones aware time series to another time zone:

```python
In [114]: ts_utc.tz_convert("US/Eastern")
Out[114]: 
2012-03-05 19:00:00-05:00    1.857704
2012-03-06 19:00:00-05:00   -1.193545
2012-03-07 19:00:00-05:00    0.677510
2012-03-08 19:00:00-05:00   -0.153931
2012-03-09 19:00:00-05:00    0.520091
dtype: float64
```

Adding a non-fixed duration (BusinessDay) to a time series:

```python
In [115]: rng
Out[115]: 
DatetimeIndex(['2012-03-06', '2012-03-07', '2012-03-08', '2012-03-09',
               '2012-03-10'],
              dtype='datetime64[us]', freq='D')

In [116]: rng + pd.offsets.BusinessDay(5)
Out[116]: 
DatetimeIndex(['2012-03-13', '2012-03-14', '2012-03-15', '2012-03-16',
               '2012-03-16'],
              dtype='datetime64[us]', freq=None)
```

## Categoricals

pandas can include categorical data in a DataFrame. For full docs, see the [categorical introduction](categorical.html#categorical) and the [API documentation](../reference/arrays.html#api-arrays-categorical).

```python
In [117]: df = pd.DataFrame(
   .....:    {"id": [1, 2, 3, 4, 5, 6], "raw_grade": ["a", "b", "b", "a", "a", "e"]}
   .....: )
   ....
```

Converting the raw grades to a categorical data type:

```python
In [118]: df["grade"] = df["raw_grade"].astype("category")

In [119]: df["grade"]
Out[119]: 
0    a
1    b
2    b
3    a
4    a
5    e
Name: grade, dtype: category
Categories (3, str): ['a', 'b', 'e']
```

Rename the categories to more meaningful names:

```python
In [120]: new_categories = ["very good", "good", "very bad"]

In [121]: df["grade"] = df["grade"].cat.rename_categories(new_categories)
```

Reorder the categories and simultaneously add the missing categories (methods under `Series.cat()` return a new Series by default):

```python
In [122]: df["grade"] = df["grade"].cat.set_categories(
   .....:    ["very bad", "bad", "medium", "good", "very good"]
   .....: )
   ....

In [123]: df["grade"]
Out[123]: 
0    very good
1         good
2         good
3    very good
4    very good
5     very bad
Name: grade, dtype: category
Categories (5, str): ['very bad', 'bad', 'medium', 'good', 'very good']
```

Sorting is per order in the categories, not lexical order:

```python
In [124]: df.sort_values(by="grade")
Out[124]: 
   id raw_grade      grade
5   6         e   very bad
1   2         b       good
2   3         b       good
0   1         a  very good
3   4         a  very good
4   5         a  very good
```

Grouping by a categorical column with `observed=False` also shows empty categories:

```python
In [125]: df.groupby("grade", observed=False).size()
Out[125]: 
grade
very bad     1
bad          0
medium       0
good         2
very good    3
dtype: int64
```

## Plotting

See the [Plotting](visualization.html#visualization) docs.

We use the standard convention for referencing the matplotlib API:

```python
In [126]: import matplotlib.pyplot as plt

In [127]: plt.close("all")
```

The `plt.close` method is used to [close](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.close.html) a figure window:

```python
In [128]: ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))

In [129]: ts = ts.cumsum()

In [130]: ts.plot();
```

**Note**: When using Jupyter, the plot will appear using `plot()`. Otherwise use [matplotlib.pyplot.show](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html) to show it or [matplotlib.pyplot.savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html) to write it to a file.

`plot()` plots all columns:

```python
In [131]: df = pd.DataFrame(
   .....:    np.random.randn(1000, 4), index=ts.index, columns=["A", "B", "C", "D"]
   .....: )
   ....

In [132]: df = df.cumsum()

In [133]: plt.figure();

In [134]: df.plot();

In [135]: plt.legend(loc='best');
```

## Importing and exporting data

See the [IO Tools](io.html#io) section.

### CSV

[Writing to a csv file:](io.html#io-store-in-csv) using `DataFrame.to_csv()`

```python
In [136]: df = pd.DataFrame(np.random.randint(0, 5, (10, 5)))

In [137]: df.to_csv("foo.csv")
```

[Reading from a csv file:](io.html#io-read-csv-table) using `read_csv()`

```python
In [138]: pd.read_csv("foo.csv")
Out[138]: 
   Unnamed: 0  0  1  2  3  4
0           0  4  3  1  1  2
1           1  1  0  2  3  2
2           2  1  4  2  1  2
3           3  0  4  0  2  2
4           4  4  2  2  3  4
5           5  4  0  4  3  1
6           6  2  1  2  0  3
7           7  4  0  4  4  4
8           8  4  4  1  0  1
9           9  0  4  3  0  3
```

### Parquet

Writing to a Parquet file:

```python
In [139]: df.to_parquet("foo.parquet")
```

Reading from a Parquet file Store using `read_parquet()`:

```python
In [140]: pd.read_parquet("foo.parquet")
Out[140]: 
   0  1  2  3  4
0  4  3  1  1  2
1  1  0  2  3  2
2  1  4  2  1  2
3  0  4  0  2  2
4  4  2  2  3  4
5  4  0  4  3  1
6  2  1  2  0  3
7  4  0  4  4  4
8  4  4  1  0  1
9  0  4  3  0  3
```

### Excel

Reading and writing to [Excel](io.html#io-excel).

Writing to an excel file using `DataFrame.to_excel()`:

```python
In [141]: df.to_excel("foo.xlsx", sheet_name="Sheet1")
```

Reading from an excel file using `read_excel()`:

```python
In [142]: pd.read_excel("foo.xlsx", "Sheet1", index_col=None, na_values=["NA"])
Out[142]: 
   Unnamed: 0  0  1  2  3  4
0           0  4  3  1  1  2
1           1  1  0  2  3  2
2           2  1  4  2  1  2
3           3  0  4  0  2  2
4           4  4  2  2  3  4
5           5  4  0  4  3  1
6           6  2  1  2  0  3
7           7  4  0  4  4  4
8           8  4  4  1  0  1
9           9  0  4  3  0  3
```

## Gotchas

If you are attempting to perform a boolean operation on a Series or DataFrame you might see an exception like:

```python
In [143]: if pd.Series([False, True, False]):
   .....:     print("I was true")
   .....: 
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-143-b27eb9c1dfc0> in ?()
----> 1 if pd.Series([False, True, False]):
      2      print("I was true")

~/work/pandas/pandas/pandas/core/generic.py in ?(self)
   1511     @final
   1512     def __bool__(self) -> NoReturn:
-> 1513         raise ValueError(
   1514             f"The truth value of a {type(self).__name__} is ambiguous. "
   1515             "Use a.empty, a.bool(), a.item(), a.any() or a.all()."
   1516         )

ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
```

See [Comparisons](basics.html#basics-compare) and [Gotchas](gotchas.html#gotchas) for an explanation and what to do.

---
Source: https://pandas.pydata.org/docs/user_guide/indexing.html

# Indexing and selecting data

The axis labeling information in pandas objects serves many purposes:

- Identifies data (i.e. provides metadata) using known indicators, important for analysis, visualization, and interactive console display.
- Enables automatic and explicit data alignment.
- Allows intuitive getting and setting of subsets of the data set.

In this section, we will focus on the final point: namely, how to slice, dice, and generally get and set subsets of pandas objects. The primary focus will be on Series and DataFrame as they have received more development attention in this area.

> Note: The Python and NumPy indexing operators `[]` and attribute operator `.` provide quick and easy access to pandas data structures across a wide range of use cases. This makes interactive work intuitive, as there's little new to learn if you already know how to deal with Python dictionaries and NumPy arrays. However, since the type of the data to be accessed isn't known in advance, directly using standard operators has some optimization limits. For production code, we recommended that you take advantage of the optimized pandas data access methods exposed in this chapter. See the MultiIndex / Advanced Indexing for MultiIndex and more advanced indexing documentation. See the cookbook for some advanced strategies.

## Different choices for indexing

Object selection has had a number of user-requested additions in order to support more explicit location based indexing. pandas now supports three types of multi-axis indexing.

`.loc` is primarily label based, but may also be used with a boolean array. `.loc` will raise `KeyError` when the items are not found. Allowed inputs are:

- A single label, e.g. `5` or `'a'` (Note that `5` is interpreted as a label of the index. This use is not an integer position along the index.).
- A list or array of labels `['a', 'b', 'c']`.
- A slice object with labels `'a':'f'` (Note that contrary to usual Python slices, both the start and the stop are included, when present in the index! See Slicing with labels and Endpoints are inclusive.)
- A boolean array (any NA values will be treated as `False`).
- A callable function with one argument (the calling Series or DataFrame) and that returns valid output for indexing (one of the above).
- A tuple of row (and column) indices whose elements are one of the above inputs.

See more at Selection by Label.

`.iloc` is primarily integer position based (from `0` to `length-1` of the axis), but may also be used with a boolean array. `.iloc` will raise `IndexError` if a requested indexer is out-of-bounds, except slice indexers which allow out-of-bounds indexing. (this conforms with Python/NumPy slice semantics). Allowed inputs are:

- An integer e.g. `5`.
- A list or array of integers `[4, 3, 0]`.
- A slice object with ints `1:7`.
- A boolean array (any NA values will be treated as `False`).
- A callable function with one argument (the calling Series or DataFrame) and that returns valid output for indexing (one of the above).
- A tuple of row (and column) indices whose elements are one of the above inputs.

See more at Selection by Position, Advanced Indexing and Advanced Hierarchical.

`.loc`, `.iloc`, and also `[]` indexing can accept a callable as indexer. See more at Selection By Callable.

> Note: Destructuring tuple keys into row (and column) indexes occurs before callables are applied, so you cannot return a tuple from a callable to index both rows and columns.

Getting values from an object with multi-axes selection uses the following notation (using `.loc` as an example, but the following applies to `.iloc` as well). Any of the axes accessors may be the null slice `:`. Axes left out of the specification are assumed to be `:`, e.g. `p.loc['a']` is equivalent to `p.loc['a', :]`.

```python
In [1]: ser = pd.Series(range(5), index=list("abcde"))

In [2]: ser.loc[["a", "c", "e"]]
Out[2]: 
a    0
c    2
e    4
dtype: int64

In [3]: df = pd.DataFrame(np.arange(25).reshape(5, 5), index=list("abcde"), columns=list("abcde"))

In [4]: df.loc[["a", "c", "e"], ["b", "d"]]
Out[4]: 
    b   d
a   1   3
c  11  13
e  21  23
```

## Basics

As mentioned when introducing the data structures in the last section, the primary function of indexing with `[]` (a.k.a. `__getitem__` for those familiar with implementing class behavior in Python) is selecting out lower-dimensional slices. The following table shows return type values when indexing pandas objects with `[]`:

| Object Type | Selection | Return Value Type |
|---|---|---|
| Series | `series[label]` | scalar value |
| DataFrame | `frame[colname]` | Series corresponding to colname |

### Slicing Ranges

Works like ndarray slicing for Series:

```python
In [37]: s[:5]
Out[37]: 
2000-01-01    0.469112
2000-01-02    1.212112
2000-01-03   -0.861849
2000-01-04    0.721555
2000-01-05   -0.424972
Freq: D, Name: A, dtype: float64
```

DataFrame slicing inside `[]` **slices the rows**:

```python
In [43]: df[:3]
Out[43]: 
                   A         B         C         D
2000-01-01 -0.282863  0.469112 -1.509059 -1.135632
2000-01-02 -0.173215  1.212112  0.119209 -1.044236
2000-01-03 -2.104569 -0.861849 -0.494929  1.071804
```

## Selection by Label

```python
In [49]: s1 = pd.Series(np.random.randn(6), index=list('abcdef'))

In [51]: s1.loc['c':]
Out[51]: 
c   -1.170299
d   -0.226169
e    0.410835
f    0.813850
dtype: float64
```

When using `.loc` with slices, if both start and stop labels are present in the index, elements located between them (inclusive) are returned.

## Selection by Position

```python
In [78]: s1 = pd.Series(np.random.randn(5), index=list(range(0, 10, 2)))

In [80]: s1.iloc[:3]
Out[80]: 
0    0.695775
2    0.341734
4    0.959726
dtype: float64
```

Out of range slice indexes are handled gracefully (like Python/NumPy):

```python
In [99]: s.iloc[4:10]
Out[99]: 
4    e
5    f
dtype: str
```

A single indexer that is out of bounds raises `IndexError`.

## Boolean Indexing

Using boolean vectors to filter data:

```python
In [168]: s = pd.Series(range(-3, 4))

In [170]: s[s > 0]
Out[170]: 
4    1
5    2
6    3
dtype: int64

In [171]: s[(s < -1) | (s > 0.5)]
Out[171]: 
0   -3
1   -2
4    1
5    2
6    3
dtype: int64

In [172]: s[~(s < 0)]
Out[172]: 
3    0
4    1
5    2
6    3
dtype: int64
```

## Indexing with isin

The `isin()` method returns a boolean vector for values in the passed list:

```python
In [185]: s = pd.Series(np.arange(5), index=np.arange(5)[::-1], dtype='int64')

In [187]: s.isin([2, 4, 6])
Out[187]: 
4    False
3    False
2     True
1    False
0     True
dtype: bool

In [188]: s[s.isin([2, 4, 6])]
Out[188]: 
2    2
0    4
dtype: int64
```

## The `where()` Method and Masking

`where()` returns data of the same shape as the original, with non-matching values replaced by NaN:

```python
In [205]: s[s > 0]
Out[205]: 
3    1
2    2
1    3
0    4
dtype: int64

In [206]: s.where(s > 0)
Out[206]: 
4    NaN
3    1.0
2    2.0
1    3.0
0    4.0
dtype: float64
```

`mask()` is the inverse boolean operation of `where()`.

## The `query()` Method

`DataFrame` objects have a `query()` method for selection using expressions:

```python
In [236]: n = 10

In [237]: df = pd.DataFrame(np.random.rand(n, 3), columns=list('abc'))

In [239]: df[(df['a'] < df['b']) & (df['b'] < df['c'])]
Out[239]: 
          a         b         c
7  0.523211  0.591538  0.792342

In [240]: df.query('(a < b) & (b < c)')
Out[240]: 
          a         b         c
7  0.523211  0.591538  0.792342
```

### The `in` and `not in` Operators

```python
In [279]: df.query('a in b')

In [281]: df.query('a not in b')
```

### Boolean Operators

```python
In [294]: df.query('~bools')

In [295]: df.query('not bools')
```

### Performance of `query()`

`DataFrame.query()` using `numexpr` is slightly faster than Python for large frames. Performance benefits are visible only with more than approximately 100,000 rows.

## Duplicate Data

Identify and remove duplicate rows using `duplicated()` and `drop_duplicates()`:

```python
In [304]: df2 = pd.DataFrame({'a': ['one', 'one', 'two', 'two', 'two', 'three', 'four'],
   .....:                    'b': ['x', 'y', 'x', 'y', 'x', 'x', 'x'],
   .....:                    'c': np.random.randn(7)})

In [306]: df2.duplicated('a')

In [309]: df2.drop_duplicates('a')
```

**`keep` parameter options:**
- `keep='first'` (default): mark/drop duplicates except for first occurrence
- `keep='last'`: mark/drop duplicates except for last occurrence
- `keep=False`: mark/drop all duplicates

## Fast Scalar Value Getting and Setting

Use `at` and `iat` for fastest scalar access:

```python
In [161]: s.iat[5]
Out[161]: np.int64(5)

In [162]: df.at[dates[5], 'A']
Out[162]: np.float64(0.1136484096888855)

In [163]: df.iat[3, 0]
Out[163]: np.float64(-0.7067711336300845)
```

## Setting with Enlargement

The `.loc/[]` operations can perform enlargement when setting a non-existent key:

```python
In [155]: dfi = pd.DataFrame(np.arange(6).reshape(3, 2),
   .....:                   columns=['A', 'B'])

In [157]: dfi.loc[:, 'C'] = dfi.loc[:, 'A']

In [159]: dfi.loc[3] = 5
```

## Selecting Random Samples

Using the `sample()` method:

```python
In [132]: s = pd.Series([0, 1, 2, 3, 4, 5])

In [133]: s.sample()  # returns 1 row

In [134]: s.sample(n=3)  # specify number of rows

In [135]: s.sample(frac=0.5)  # specify fraction of rows
```

## Index Objects

The `Index` class and its subclasses can be viewed as implementing an _ordered multiset_. Duplicates are allowed.

### Set Operations on Index Objects

```python
In [352]: a = pd.Index(['c', 'b', 'a'])

In [353]: b = pd.Index(['c', 'e', 'd'])

In [354]: a.difference(b)
Out[354]: Index(['a', 'b'], dtype='str')

In [357]: idx1.symmetric_difference(idx2)
Out[357]: Index([1, 5], dtype='int64')
```

> **Note**: The resulting index from a set operation will be sorted in ascending order.
