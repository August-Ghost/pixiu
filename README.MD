# 貔貅-电子货币量化交易平台
‘貔貅’是一个基于Tornado实现的电子货币量化交易平台，通过统一的数据接口，
让大家可以更加专注于交易策略的实现。目前完美支持[火币网](https://www.huobi.com/),
更多交易平台后期将陆续支持。文档还需慢慢完善，所以有未写清楚的地方就暂时委屈下大家看看源代码吧QAQ.
<br>不过量化交易重心在于交易策略而不是工具。貔貅虽聚财，当心被反噬。
<br>Anyway, good hunting!
## Feature
* 非阻塞实现，轻量高效
* 可支持多交易网站
* 易于扩展
* 集成常用公式（更多公式敬请期待）
* 支持模拟交易（虽然略粗糙）
## Usage

    pixiu.py [-h | --help]
    pixiu.py start [-d | --debug ][-l | --syslog <syslog>][-v | --verbose][--loghome <loghome>][--pycurl]
    pixiu.py traceback [-d | --debug ][-l | --syslog <syslog>][-v | --verbose][--loghome <loghome>][--pycurl]
    pixiu.py create datasource <name> <dst>
    pixiu.py create strategy <name> <dst>
    
## Option

    -h --help    Show help message.
    -d --debug    Debug flag. Set if debug info is desired. Default to False. [default: False]
    -l --syslog <syslog>     Set system log file.
    -v --verbose    Set if logging to stdout is needed.
    --pycurl    Set if tornado.curl_httpclient.CurlAsyncHTTPClient is preferred.
    --loghome <loghome>    Set the path to store logs. [default: ./log]
    start   Start system in normal mode.
    traceback Start system in traceback mode(coming soon).
    create datasource <name> <dst> Create a datasource from template in current.
    create strategy <name> <dst> Create a strategy from template in destination.

## Dependency
建议使用[conda](https://conda.io/miniconda.html)管理Package和Python虚拟环境
<br>[为conda添加国内源](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
<br>Python: 3.6.x
<br>Docopt: >= 0.6.2
<br>Tornado: >= 4.5.1
<br>(Optional)Numpy: >= 1.12.1
<br>(Optional)Pandas: >= 0.20.1
<br>(Optional)Pycurl: >= 7.43.0 

## Quick Guide

### 添加数据源
 以添加火币网莱特币3分钟K线为例。

创建数据源模板

 ```text
pixiu.py create datasource huobi_ltc_kline_3min .
```

会在当前目录下创建一个名为huobi_ltc_kline_3min.py的数据源模板

    # -*- coding: utf-8 -*-
    from mainframe.ecdatasource import ECDataSource
    
    
    class ECDataSource_huobi_ltc_kline_3min(ECDataSource):
        def config(self):
            self.configure = {
                "name": "huobi_ltc_kline_3min",  # Required. Your strategy need this to get data.
    
                # Remove the comment if you want to deliver logs into separated files.
                # By default, logs will be delivered into log/ECDatasource_error.log
                # and log/ECDatasource_debug.log
                #"datasource_logging":{
                #    "if_debug": False,
                #   # Optional, the debug log file. If ignored, default will be "log/ECDataSource.$name_debug.log"
                #    "dbglog": r"",
                #    # Optional, the errorlog file. If ignored, default will be "log/ECDataSource.$name_error.log"
                #    "errlog": r"",
                #},
                # Remove the comment if you want to deliver logs into separated files.
                # By default, logs will be delivered into log/ECInterface_error.log
                # and log/ECInterface_debug.log
                #"interface_logging": {
                #    "if_debug": False,
                #    # Optional, the debug log file. If ignored, default will be "log/ECInterface.$name_debug.log"
                #    "dbglog": r"",
                #    # Optional, the debug log file. If ignored, default will be "log/ECInterface.$name_error.log"
                #    "errlog": r"",
                #},
    
                "query_config":{
                    "url": r"", # The url to fetch data.
                    "method": "GET"
                    # For more additional parameters, please refer to:
                    # http://www.tornadoweb.org/en/stable/httpclient.html#request-objects
                },
         }

        def after_init(self):
         """
         Will be called after datasource initiated.
         :return:
         """
         pass

        async def __call__(self, **kargs):
            # Overwrite it if you need some hacks while calling datasource.
            return super(ECDataSource, self).__call__(**kargs)

        async def process_response(self, response):
            # Overwrite it if additional workaround is necessary to process response.
            return response
    EXPORT = ECDataSource_huobi_ltc_kline_3min
    
<br>类名可随意修改，但是必须与EXPORT一致。配置项name是策略调用数据源的依据，必须唯一。
<br>这里使用实现的火币网API生成模块生成访问地址。将query_config替换为以下：

    "query_config": {
        api": HuobiAPI_LTC_BTC().stock(market="CNY").ltc_kline_001_json,
        },

<br>重写__call__。 __call__方法的参数即为策略在调用数据源时的参数：

    async def __call__(self, **params):
        p = {**params}
        if "length" not in params:
            p["length"] = 1
        p["length"] = min(p["length"] * 3, 2000)

        raw = self.configure["query_config"]["api"](**p)
        query_param = {**raw,
                       "url": raw["url"] + "?" + raw["params"], }
        del query_param["params"]
    
        return await self.query(**query_param)
        
<br>重写process_response。在process_response方法中你将对服务器返回结果按自己意愿进行加工：

    def parse_json(self, json_response):
        return tuple({"timestamp": int(datetime.strptime(j[0][:-5],
                                                         "%Y%m%d%H%M").timestamp()),
                      "open": j[1],
                      "high": j[2],
                      "low": j[3],
                      "close": j[4],
                      "vol": j[5], } for j in json_response)

    async def process_response(self, response):
        parsed = self.parse_json(json.loads(response))
        data_df = DataFrame.from_records(parsed)
        # Is there any better solution?
        result = tuple({"timestamp": df["timestamp"].max(),
                        "open": df[df["timestamp"] == df["timestamp"].min()]["open"].iloc[0],
                        "high": df["high"].max(),
                        "low": df["low"].min(),
                        "close": df[df["timestamp"] == df["timestamp"].max()]["close"].iloc[0],
                        "vol": df["vol"].sum()} for df in (data_df.iloc[chunk_id * 3: chunk_id * 3 + 3] for chunk_id in range(0, len(parsed) // 3)))
        return result

<br>最终完成的数据源如下：

    # -*- coding: utf-8 -*-
    from mainframe.ecdatasource import ECDataSource
    from api.huobi_api import HuobiAPI_LTC_BTC
    from pandas import DataFrame
    from datetime import datetime
    import json


    class Huobi_Ltc_kline_3min(ECDataSource):
        def config(self):
            self.configure = {
               "name": "huobi_ltc_kline_3min",  # Required. Your strategy need this to get data.

                "query_config": {
                    "api": HuobiAPI_LTC_BTC().stock(market="CNY").ltc_kline_001_json,
                },
            }

        async def __call__(self, **params):
            p = {**params}
            if "length" not in params:
                p["length"] = 1
            p["length"] = min(p["length"] * 3, 2000)

            raw = self.configure["query_config"]["api"](**p)
            query_param = {**raw,
                           "url": raw["url"] + "?" + raw["params"], }
            del query_param["params"]

            return await self.query(**query_param)

        def parse_json(self, json_response):
            return tuple({"timestamp": int(datetime.strptime(j[0][:-5],
                                                            "%Y%m%d%H%M").timestamp()),
                        "open": j[1],
                        "high": j[2],
                        "low": j[3],
                        "close": j[4],
                        "vol": j[5], } for j in json_response)

        async def process_response(self, response):
            parsed = self.parse_json(json.loads(response))
            data_df = DataFrame.from_records(parsed)
            # Is there any better solution?
            result = tuple({"timestamp": df["timestamp"].max(),
                            "open": df[df["timestamp"] == df["timestamp"].min()]["open"].iloc[0],
                            "high": df["high"].max(),
                            "low": df["low"].min(),
                            "close": df[df["timestamp"] == df["timestamp"].max()]["close"].iloc[0],
                            "vol": df["vol"].sum()} for df in (data_df.iloc[chunk_id * 3: chunk_id * 3 + 3] for chunk_id in range(0, len(parsed) // 3)))
            return result

### 创建策略
创建策略模板
 ```text
pixiu.py create strategy index_test.
```
<br>会在当前目录下创建一个名为index_test.py的数据源模板:

    # -*- coding:utf-8 -*-
    from mainframe.ecstrategy import ECTradeStrategy


    class TradeStrategy_index_test(ECTradeStrategy):
        async def init(self):
            # Init strategy, like setting up index you need.
            # By default, your strategy will be called every seconds.
            # If set period to 0, the strategy will only be called once.
            self.period = 1000 # msecond.
            
        async def cold_start(self):
            """
            Will be called only once before the first time the strategy run.
            It is strongly recommended to 'warming up'  the indexes for the
            sake of accuracy.
            :return:
            """
            pass

        async def process(self):
            # Write your strategy here.
            # Good hunting :)
            pass


    EXPORT = TradeStrategy_index_test
    
<br>这里以打印火币网莱特币1分钟K线的5周期均量线（MA5）为例。
<br>在init方法里初始化MA5:

    def init(self):
        # Init strategy, like setting up index you need.
        # By default, your strategy will be called every seconds.
        # If set period to 0, the strategy will only be called once.
        self.period = 1000 # msecond.
        self.ma = MA(5)

<br>在cold_start里获取足量历史数据对公式进行预热以降低误差：

    async def cold_start(self):
        # Use historical data to activate the index
        init_data = await self.huobi_ltc_kline_1min(length=2000)
        for i in init_data[:-1]:
            # Separate timestamp
            self.ma((i["timestamp"], i["close"]))
            
<br>将策略逻辑在process里实现:

    async def process(self):
        # Write your strategy here.
        # Good hunting :)
        data = await self.huobi_ltc_ticker()
        # Separate timestamp
        print(self.ma((data["timestamp"], data["close"])))
        
<br>最终完成的策略:

    # -*- coding:utf-8 -*-
    from mainframe.ecstrategy import ECTradeStrategy
    from index.ma import MA


    class TradeStrategy_index_test(ECTradeStrategy):
        def init(self):
            # Init strategy, like setting up index you need.
            # By default, your strategy will be called every seconds.
            # If set period to 0, the strategy will only be called once.
            self.period = 1000 # msecond.
            self.ma = MA(5)

        async def cold_start(self):
            # Use historical data to activate the index
            init_data = await self.huobi_ltc_kline_1min(length=2000)
            for i in init_data[:-1]:
                # Separate timestamp
                self.ma((i["timestamp"], i["close"]))

        async def process(self):
            # Write your strategy here.
            # Good hunting :)
            data = await self.huobi_ltc_ticker()
            # Separate timestamp
            print(self.ma((data["timestamp"], data["close"])))


    EXPORT = TradeStrategy_index_test

更多公式详见index目录。

### 交易

#### 实盘交易

以火币网为例。
<br>平台已内置了火币网交易支持，目前仅支持比特币和莱特币的交易。在trader目录下创建如下文件:

    from trader.huobi_trader import Huobi_Trader

    class Huobi_test_trader(Huobi_Trader):
        def config(self):
            self.configure = {
                "access_key": "your access_key",
                "secret_key": "your secret_key",
          }

填入你的access_key和secret_key，然后再策略里import并实例化即可。
<br>支持的方法可参见trader/huobi_trader.py源代码和官方github[文档](https://github.com/huobiapi/API_Docs/wiki)。

#### 模拟交易

模拟交易目前仅支持按照买一卖一价格全量立即成交。
<br>在策略里import Huobi_SimpleDummyTrader即可使用。默认现金100000元。
<br>示例如下:

    from trader.huobi_dummytrader import Huobi_SimpleDummyTrader
    
    class TradeStrategy_index_test(ECTradeStrategy):
        def init(self):
            # Init strategy, like setting up index you need.
            # By default, your strategy will be called every seconds.
            # If set period to 0, the strategy will only be called once.
            self.period = 1000 # msecond.
            self.ma = MA(5)
            self.trader = Huobi_SimpleDummyTrader(currency=10000)
            
        async def process(self):
            # Write your strategy here.
            # Good hunting :)
            data = await self.huobi_ltc_ticker()
            # Separate timestamp
            print(self.ma((data["timestamp"], data["close"])))
            print(await self.trader.buy(coin_type=2))

#### 回测交易

回测交易将以给定价格全量成交。只需在交易（sell、buy）时传入参数price即可。
详情请参见trader/huobi_dummytrader.py。

## Advanced Guide

Coming Soon :)

## Logging&Debugging

启动平台时建议加上-v参数，将会把错误信息输入值stdout。启动平台时加上-d参数将会开启调试模式，详细记录每一次请求。
log目录下三个默认的日志文件:
<br>ECDataSource_error.log: 记录所有DataSource中产生的错误；
<br>ECInterface_error.log: 记录所有Interface中产生的错误；
<br>sys.log: 记录系统运行过程中产生的错误；

在启动平台时-d -v等参数为全局设置，你仍然可以给每一个DataSource和Interface配置单独的日志参数如下:
    
    # By default, logs will be delivered into log/ECDatasource_error.log
    # and log/ECDatasource_debug.log
    "datasource_logging":{
        if_debug": False,
        # Optional, the debug log file. If ignored, default will be "log/ECDataSource.$name_debug.log"
        dbglog": r"",
        # Optional, the errorlog file. If ignored, default will be "log/ECDataSource.$name_error.log"
        errlog": r"",
        },
    # By default, logs will be delivered into log/ECInterface_error.log
    # and log/ECInterface_debug.log
    "interface_logging": {
        if_debug": False,
        # Optional, the debug log file. If ignored, default will be "log/ECInterface.$name_debug.log"
        dbglog": r"",
        # Optional, the debug log file. If ignored, default will be "log/ECInterface.$name_error.log"
        errlog": r"",
        },


## FAQ
1. 如何调用数据源？
<br>每个数据源在创建时有一个name属性，在策略中使用self. + 数据源name属性进行调用。
以调用火币网莱特币3分钟K线为例，使用awaite self.huobi_ltc_kline_3min()即可调用。
注意每个数据源都是callable对象，调用时可以传入参数，例如length。

2. 如何进行回测？
<br>目前的实现并不能直接进行回测。不过通过一点技巧即可达到回测的效果。
将策略period设置为0，请求足量历史数据并保存，然后通过迭代器进行迭代。

## TroubleShooting

### TypeError: 'coroutine' object is not subscriptable

常见的情况如下:
````
tsmp = await self.huobi_ltc_ticker()["timestamp"]
````

subscrip运算符优先于await运算符与self.huobi_ltc_ticker()结合，因此正确的调用形式如下:
````
tsmp = (await self.huobi_ltc_ticker())["timestamp"]
````

### AttributeError: No datasource named xxx
在策略中调用数据源时使用的名字与数据源name属性不符。
注意调用数据源时使用的是数据源的name属性，而不是类名。

### 策略未运行（找不到数据源）
检查是否误删除EXPORT变量。

## Todo
* 更完善的文档与注释
* 完善的回测系统的实现与行情数据的积累
* 更加精确的模拟交易