# 处理 sabic 数据

## 使用方法

### 安装环境

在项目根目录安装项目依赖环境

```shell script
pipenv install --skip-lock
```

### 开始使用

1. 增加运行配置

配置文件在项目目录下的 `config/`。

具体使用参考 [程序运行配置](#程序运行配置)

2. 添加数据文件

数据文件在项目目录下的 `data/`。

```
.
├── data
│   └── 20200416
│       ├── output
│       │   └── 39014090-20200416195656.xlsx
│       ├── raw
│       │   └── 39014090.xlsx
│       └── wordbag
│           └── 词典库_39074000_v22.xlsx
```

数据文件存放方式为：

- `data/20200416/raw/39014090.xlsx` 为原始数据文件位置
- `data/20200416/wordbag/词典库_39074000_v22.xlsx` 为词典文件存放为止
- `data/20200416/output/39014090-20200416195656.xlsx` 为处理后数据存放目录

其中 `20200416` 是根据需求自己创建的目录，这里称作日期目录。 日期目录下面的目录除了 `output` 为请手动创建后添加数据文件。

3. 修改程序配置信息

打开项目根目录下的 `run.py` 文件，修改 `date_path` 和 `config_filename` 两个变量。

`date_path` 为上一步配置的日期目录，`config_filename` 为第一步增加的运行配置文件名称

4. 运行程序

```shell script
pipenv run python run.py
```

程序运行的时候会有日志信息输出，方便查看进度和错误诊断。

终端程序，直接时候用 `Ctrl+c` 即可。一次不行连续按三次。


## 配置

### 项目配置

项目代码提供部分配置，用来修改项目运行信息，方便使用。

TODO

### 程序运行配置

运行配置使用 YAML 格式。具体使用方法请参考 [YAML 文档](https://yaml.org/)

如果比较熟悉 JSON 数据格式，可以将配置粘贴到 [YAML TO JSON](https://www.json2yaml.com/convert-yaml-to-json) 中检查。

#### 如何配置？

程序运行的时候，会有一个 `config_filename` 的参数，可根据使用场景以不同的文件命名方式区分不同的配置。
如 `2020-04-12.yml` 表示 2020年4月12日运行的数据配置。或者 `20200412153300-temporary.yml` 表示 2020年4月12日15点33分运行的临时
配置。命名规则根据自己需求来就行啦，但最好找到一种好用好区分的格式，或者使用一份外部文件做记录。

**示例配置：**

```yaml
%YAML 1.2
---

- raw:
    filename: 39014090.xlsx
    sheet: Sheet1
    col_name: 规格
  wordbag:
    filename: &filename1 词典库_39074000_v22.xlsx
    supplier:
      filename: *filename1
      sheet: supplier_供应商
      key_index: 0
      value_index: 1
    brand:
      filename: *filename1
      sheet: brand_品牌
      key_index: 0
      value_index: 1
    grade:
      filename: *filename1
      sheet: grade_牌号
      key_index: 0
      value_index: 1
    quality:
      filename: *filename1
      sheet: quality
      key_index: 0
      value_index: 1
    grade_to_supplier:
      filename: *filename1
      sheet: grade_to_supplier
      key_index: 0
      value_index: 1
    grade_to_brand:
      filename: *filename1
      sheet: grade_to_brand
      key_index: 0
      value_index: 1
    brand_to_supplier:
      filename: *filename1
      sheet: brand_to_supplier
      key_index: 0
      value_index: 1
```

配置文件中的字段名(冒号前面的单词)请勿更改，否则将影响程序正常执行。，字段值(冒号后面的单词) 根据情况更改。

字段值中带有 `&` 和 `*` 的内容为引用变量。使用 `&` 为定义被引用变量。如 `&filename1` 定义了一个引用变量。使用 `*` 引用前面定义的变量，
如 `*filename1` 引用了前面定义的变量。

这个也是根据需求来，如果某个节点的元数据配置不在同一个文件中，可以删除引用单个配置，如果都在一个文件中，就使用引用前面的配置，方便统一
更改。

一般情况下只要根据实际情况更改 `filename` 变量即可。而且根据当前规则(当前时间：2020-04-16) 字典元信息都是放在一个文件中的，直接修改
最前的两个 `filename` 即可。

在配置中还有其他字段，如 `sheet` ，表示数据在文件的某个 sheet 中。 `key_index` 和 `value_index` 表示字典 key-value 对应的列序号，
默认从 0 开始，即第一列为 key 值在第一列 `key_index` 就是 0。 `col_name` 是 规格数据 所在的列名称。

**注意：** 所有数据文件均要有表头，否则确实第一行数据。对于原始数据文件，会导致列名错误无法运行。

##### 词典库规则配置



```yaml
  wordbag:
    filename: &filename1 词典库_39074000_v22.xlsx
    supplier:
      filename: *filename1
      sheet: supplier_供应商
      key_index: 0
      value_index: 1
    brand:
      filename: *filename1
      sheet: brand_品牌
      key_index: 0
      value_index: 1
```

上面配置片段中， `wordbag` 下面有两个规则，分别是 `supplier` 和 `brand` 。在程序运行的时候，会根据配置的这两个词典数据处理这两类数据。
如果不想处理某些规则的数据只需要将该节点下的内容删除举行了。

比如现在只处理 `brand` 的数据，规则就是这样的。

```yaml
  wordbag:
    filename: &filename1 词典库_39074000_v22.xlsx
    brand:
      filename: *filename1
      sheet: brand_品牌
      key_index: 0
      value_index: 1
```

##### 多数据同时运行

上面示例配置只能运行一个数据文件，如果多个数据文件同时运行，将顶层节点 `- raw:` 以下的所有内容复制然后粘贴到后面就行了。在 YAML 中 `- `
代表列表的一个元素，如果同一级别有多个 `-`，则是多个元素。具体参考 [`default.yml`](./config/default.yml)。

## TODO

- [ ] 增加命令行调用
- [ ] 增加读取自定义配置目录
- [ ] 增加用户自定义配置覆盖默认配置
