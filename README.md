# LLM-Knowledge-Database-with-Low-Hardware-Requirements<img src=".\pics\degu.png"  align="right" style="margin-top: 10px;margin-right: 20px;" width = "150" height = "150"/>
LLM-Knowledge-Database-with-Low-Hardware-Requirements.                                                                                   

## 前言

Introduction



如今（2023）大模型越来越多地被应用到生产生活中，然而大模型本身需要的算力开销很大，往往非个人用户所能承受。比如我最开始做大模型知识库的时候，想用清华的ChatGLM2-6B。即使使用训练好的模型，使用最低的精度（INT4），依然无法提供足够的显存支持模型运行。另一方面，使用现有的大模型接口往往并非免费，而且在某些国家和地区（例如中国大陆），很难方便地获取服务。

Nowadays (2023), LLMs are increasingly being applied in production and daily life. However, LLMs themselves require significant computational resources, which are often beyond the reach of individual users. For example, when I first started building an LLM knowledge base, I wanted to use ChatGLM2-6B from Tsinghua University. Even with a pre-trained model and using the lowest precision (INT4), there was still insufficient GPU memory to support the model's execution. Additionally, existing LLM interfaces are often not free to use, and accessing these services can be inconvenient in certain countries and regions, such as mainland China.

知识库是LLM的一个常见的应用，相比于查询繁多的文件，大模型驱动知识库如同一个客服，可以让用户更方便快捷地获得对应的知识，在企业管理、教育等方面有很大的实用价值。

A knowledge base is a common application of LLMs. Compared to searching through numerous documents, an LLM-driven knowledge base acts as a virtual assistant, allowing users to conveniently and quickly obtain the desired information. It has great practical value in areas such as enterprise management and education.

因此，本项目旨在让每一个普通用户在较差的硬件条件下享受大模型的便利，轻松地构建一个大模型知识库。后续我还会基于本项目开发升级的应用，在安全等方面进行进一步探索。

Therefore, the aim of this project is to enable every ordinary user to enjoy the convenience of LLMs even with limited hardware resources, making it effortless to build an LLM knowledge base. Furthermore, I will develop and upgrade applications based on this project to explore further advancements in areas like security.

本项目仍在开发中，请持续关注最新进展，欢迎学习交流。

This project is still under development, so please stay tuned for the latest updates and feel free to engage in learning and discussions.





## 版本0.0.1（day3morning）

实现了大模型知识库全流程成功运行。当前功能：输入一个pdf文档，回答相关问题。运行方法：python harness.py

<img src=".\pics\yuanlitu.jpg" style="zoom: 25%;" />

实现原理：

使用Langchain开发，包括读取文件、分词、embedding、向量比较、套用prompt、大模型调用步骤。POE.py中为一个从poe.com获取数据的爬虫，用于实现大模型调用。embedding采用的是huggingface上的intfloat_multilingual-e5-base。





## 版本0.0.2（day3afternoon）

相较于v0.0.1更**优雅**的实现，进行了函数封装等重构。同时新增了以下新功能：

1. 实现了多个pdf文本的输入，同时能识别子文件夹下的文件
2. 可以自定义问题，与机器人进行多轮对话

运行方法：python harness.py

variables里编辑变量

llm_agent里编辑prompt

聊天时使用!clear清除记录，使用!quit结束对话



## 版本0.0.3 （day4afternoon）

新增了数据重用功能，如果选择重用数据会直接进入对话阶段

运行方法同v0.0.2



## 版本0.1.0 （day4afternoon）

<img src=".\pics\structv010.jpg" style="zoom: 50%;" />

采用新结构的v0.1.0，参考推荐系统中的召回->粗排->精排->重排的模式，将本地低算力的embedding和词向量匹配作为精度低速度快的召回/粗排，LLM作为精排。此版本实现方法为依次问LLM内容与问题是否相关，如果答案为否，则输入下一条。这个prompt同样可以在llm_agent里编辑。

新结构给embedding部分一定的容错空间，提升准确率。在实验中起到了一定的成效。

其余小变动：新增了统一的异常报错函数；词向量上下文范围和召回数量可以在variables里边编辑；新增无法回答时的标准输出。

## 版本0.1.1 （day5morning）

主要更新：新增了引用功能，在给出回答的同时给出参考的源文件和页码。因为扩大搜索范围的影响，目前页码可能有最大2页左右的误差。该功能可辅助用户去查阅源文件获取更详细的信息，同时作为后续访问控制功能的基础。

其余小变动：变量新增了DEBUG参数，可以选择是否开启调试输出；优化算法，避免了先前版本多次相似度匹配导致的高时间复杂度问题；修正了上一版本原理图中的错别字问题。

## 版本0.1.2 （day5afternoon）

主要更新：多模态文件输入功能，支持'pdf','docx','pptx','txt','md','png'多种类型的文件。后续可能的新文件类型包括url、youtube视频、bilibili视频等。这里的png指包含文字的图片，具体实现使用pytesseract库进行文字识别录入。

其余小变动：新的环境文件；优化了print的内容。

## 版本0.1.3 （day6afternoon）

主要更新：知识库源文件夹支持增量扩展知识库，即增加新文件时不用全部embedding，只处理部分数据。减少文件或用户要求时才执行完整的start over。部分重构了切分文件和主文件的代码，更加模块化。新增了对比文件的util。

其余小变动：新的可调整变量。

## 版本0.1.4 （day8morning）

主要更新：由于poe接口变动，原先的poe爬虫无法正常运行了。为了防止此类情况再次出现，此次版本更新去除了爬虫，新增了由@snowby666开发的poe-api-driver以及@ghost-in-a-shell开发的基于selenium的爬虫。速度较慢的selenium爬虫作为备份，未实际连接到主体代码。***注意：这意味着v0.1.3及之前版本代码无法正常运行！！！***后续会基于v0.1.1发布一个长期版用于prompt测试等。

其余小变动：variables变动，使用新爬虫需要新的变量

## 版本0.1.1稳定版

长期稳定运行的版本，用于prompt测试等。使用了新的poe爬虫，**是0.1.3及之前唯一可用版本**。然而，经过测试，我们不得不承认**v0.1提出的reject设计是比较失败的**，新的解决方案正在构思中。

## 版本0.1.5

主要更新：将大模型的调用封装成了langchain的llm类，更加标准化的实现。同时进行了一些传统nlp应用的尝试，使用的是HanLP的实现。后续希望探索包括agent，传统nlp意图识别在内的多种方法。

