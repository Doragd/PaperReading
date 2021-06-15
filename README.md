# :memo: Paper Reading

> 2021-6-3: 创建了本仓库
>
> 问渠哪得清如许 为有源头活水来

## :dart: Calendar

* 2021/6

|    Mon    |        Tue        |         Wed         |      Thu       |            Fri             |    Sat     | Sun  |
| :-------: | :---------------: | :-----------------: | :------------: | :------------------------: | :--------: | :--: |
|    31     |         1         |          2          | 3:sweat_drops: | 4:triangular_flag_on_post: | 5:pensive: |  6   |
| 7:accept: | 8:deciduous_tree: | 9:heavy_check_mark: |       10       |             11             |     12     |  13  |
|    14     |      15:ok:       |         16          |       17       |             18             |     19     |  20  |
|    21     |        22         |         23          |       24       |             25             |     26     |  27  |
|    28     |        29         |         30          |       1        |             2              |     3      |  4   |

##  :game_die: Notes

### 数据集

* Figurative Language in Recognizing Textual Entailment，ACL 2021 Findings
  * NLI任务的新数据集，涉及到了明喻识别，暗喻识别和讽刺识别，感觉挺难的，在MNLI上微调的roberta-large表现不太行，尤其是在涉及到需要词汇知识和语用推理的example上面。
  * 思考：没啥感想，看看以后能不能用来测试文本分类，感觉需要引入额外的知识来判断

### 机器翻译

* Neural Machine Translation with Monolingual Translation Memory，ACL2021

  ![image-20210615160530256](https://img2020.cnblogs.com/blog/1098855/202106/1098855-20210615160533670-1655798094.png)

  * 实际做的是retrieve+generate框架的事情：给定源语言-目标语言的paired data + 目标语言的target data(作为检索库)，执行机器翻译
  * 优点：提出了一种retriever和generator是端到端联合优化的方案；在低资源和跨领域上(实际需要all domains的data一起训练，好处是不用再进行domain-specific training)表现很好；用跨语言对齐来解决联合优化中retriever的冷启动问题
  * 以后读论文：不要浅尝辄止！否则没什么用啊！

### 问答系统

* A Semantic-based Method for Unsupervised Commonsense Question Answering，ACL2021，:star:

  ![image-20210604154358072](https://img2020.cnblogs.com/blog/1098855/202106/1098855-20210604154357999-124516299.png)

  * 无监督常识问答，即给一个问题和多个选项，选出最正确的，不过并没有标注数据。以前的方式是用pretrained model去为多个选项打分，但是容易受到攻击。这里提出用生成预训练模型去生成可能的答案，再去度量和多个选项之间的距离，看哪个靠的更近。没有读完这篇文章，但是我觉得有趣的是这个打分函数的设计，用了之前用过的vMF-VAE，不过我还没仔细看过。后续还测试了经受攻击的能力。这种用生成去做无监督QA的方式还是很有意思。
  * 思考：其实我觉得可能可以用到我的那个项目上去。。。还要再思考下。这个任务也挺有意思的。

### 常识生成

* Retrieval Enhanced Model for Commonsense Generation，ACL2021
  * 常识生成：给定一组概念，生成一句不违背常识和语法，且包含所有概念的句子
    * https://inklab.usc.edu/CommonGen/leaderboard.html
  * retrieve-and-generate范式：
    * 伪concept-sentence预训练：从额外的语料库中提取句子和句子的concept，作预训练
    * 检索：一种是rule-based匹配，要求检索的句子包含尽量多的目标concept，一种是trainable检索，可训练的检索器。rule-based的坏处在于倾向于去检索更长的句子，很可能不是我们想要的。相比于fan的工作，这篇主要就是提出预训练阶段也要应用检索，微调阶段要可训练地检索
  * 思考：好吧， 这个榜单太卷了。。虽然有点想法，但是不确保能超过。

###  文本摘要

* SimCLS: A Simple Framework for Contrastive Learning of Abstractive Summarization，ACL2021

  * 这篇文章是讲怎么用对比学习的范式去缓解生成过程中的曝光偏差：训练和测试之间的不一致，首先是teacher forcing问题，测试时没有groundtruth，其次是局部预测，全局评估，MLE的训练目标和评测指标并不完全一致。

  * 给定一个groundtruth，我们生成的目标肯定是要让生成的文本，与这个groundtruth在某个评价指标下分数尽量高。新的做法是分成两阶段：一个生成模型去生成候选文本，一个评估模型去打分score，选择最好的候选文本。也就是生成的时候，通过sampling去生成多个候选项，然后用roberta编码document和生成文本，正样本是和groundtruth相似度最高的。

  * 其实借鉴的quality estimation的思想，更好的候选摘要 应该获得更高的质量分数 w.r.t 源文档 D

  * 同时实验验证了一件事，sample多个candidate，取最大的rouge的那个样本，可以获得更好的分数！

    

* Demoting the Lead Bias in News Summarization via Alternating Adversarial Learning，ACL2021，:star:
  * 抽取式摘要在一些特定领域数据上往往会有一些bias，比如news数据上，一般新闻摘要数据上，靠前的句子一般都是主旨句，也就是可以选取作为summary。不过每个数据集的bias程度并不一样，不能完全依赖这种bias来设计模型，理想中应该按照句子语义来确定。之前的方式就是去shuffle句子，这样会丢失句子之间的联系信息。这篇文章研究的就是如何设计encoder，使得编码的特征能够尽量不包含句子的位置信息，从而使得预测时候对位置信息减少依赖性。但同时，对于一些bias比较重的，严重依赖位置bias的数据集不能性能降太多。否则的话，直接把position embedding去掉不就可以不包含位置信息了吗。这篇的亮点就是设计对抗方式让encoder尽快不包含位置信息，亮点在于多个MLP的使用和与均匀分布的拉近：
  * 典型但是又有些不同的对抗学习：
    1.阶段1.固定预训练摘要模型，训练predictor去预测句子在文档中位置
    2.阶段2..固定predictor，去更新摘要模型使得对抗预测loss最大化。
    注意到：这里实际并不是最大化熵的形式。而是假定当预测不出来时，predictor应该落入一个平凡解，也就是等概率预测每个位置，即预测概率分布是一个均匀分布。所以相当于最小化两个分布之间的距离。
  * 对每个位置的预测都采用相同的MLP会导致位置信息采用其他方式去编码，为了避免这种情况，所以对每个位置分别去用一个MLP去预测，让encoder难以通过其他隐式编码方式来保持句子的位置信息！
  * 思考：可能这种对抗方式可以用来过滤位置信息，不过？位置信息不是可以通过去掉position embedding来去掉吗？

### 信息抽取

* AdaTag: Multi-Attribute Value Extraction from Product Profiles with Adaptive Decoding，ACL2021，:star:

  ![image-20210607135820821](https://img2020.cnblogs.com/blog/1098855/202106/1098855-20210607135820797-730617993.png)

  * 多属性值抽取：给定一个text，和一个query（需要提取的属性），输出属性值。建模为序列标注任务。
  * 创新点：提出了一种类似shared-private的结构，一方面各种属性之间的信息共享能够为当前属性消除歧义，另一方面属性独有的特征也能被捕捉
    * 所有属性共享一个统一的文本编码器，以便通过学习不同的子任务来增强表示，并且每个属性都有一个适合其对应子任务的解码器，其参数基于属性信息
    * shared：用一个共享的text encoder去编码text
    * private：提出一种adaptive crf decoder，利用超网络和MOE机制，根据attribute embedding去生成特有的crf decoder
  * 思考：这种结构可以去生成特定于某种attribute的网络layer，并通过MOE去集成

### 问题生成

* Factorising Meaning and Form for Intent-Preserving Paraphrasing，ACL2021，:star:

  ![image-20210607112730225](https://img2020.cnblogs.com/blog/1098855/202106/1098855-20210607112732162-10741629.png)

  * 实际做的就是限制下问题生成任务上的句法可控的文本复述生成，也是用的解纠缠那一套，即生成句法不同（也就是surface form）但是语义相同(相同的intent，即可以得到相同的回答)的问题
  * 创新点：
    * 把复述生成限制到比较有应用场景的问题生成上
    * 以前的句法可控文本复述生成是给定了target form的，这里直接infer出不同的target form
    * VQ-VAE：用连续隐变量表示语义，用离散隐变量表示form（动机：问题的形式是比较有限的）
    * 理论：information bottleneck + disentanglement
  * 思考：又一篇disentanglement的文章

### 多模态

* Maria: A Visual Experience Powered Conversational Agent, ACL2021
  * visual grounded conversation
  * 有趣的点是表示一些常识无法通过KG来获得，而是要通过visual experience，也就是大量图像
  * 针对传统的visual conversation需要paired image的问题，将其扩展到从大规模open-end的图像中检索，实现zero-resource image grounded dialog
  * 提了一个对齐视觉信号和融入视觉信息的生成的方法
* Unpaired Cross-lingual Image Caption Generation with Self-Supervised Rewards，MM2020
  * unpaired 跨语言图像描述：只给了源语言的paired data。目标语言的依靠一个现成的翻译模型来生成伪平行语料。这篇解决的是，在伪平行语料上训练时，如何缓解伪平行语料的噪声，因为并不一定是visual relevancy。提了两个reward：一个是流畅度，用在目标语言的单语语料库的LM去评测。还有一个是视觉和语言的对齐：实际也是在伪平行语料上去对齐，说其实这里面也有很多视觉相关的句子。先去训练一个匹配模型VSE。此时reward就靠这个模型给。
* Good for Misconceived Reasons: An Empirical Revisiting on the Need for Visual Context in Multimodal Machine Translation，ACL2021
  * 多模态机器翻译指在纯文本机器翻译中加入相关的visual context信息来增强翻译效果（两种方式：一种给定源文本和一张相关图片，生成目标文本，一种是给定源文本，去检索一些相关图像，结合起来生成目标文本），实际很多人就在质疑到底需不需要visual context。以前的研究方法是把相关图像替换成随机图像来看效果变化，但实际上这种方式并不能直接看出到底需不需要visual context。这篇文章其实就是提出一个gate机制，把visual context通过一个gate去传入模型，最后检查gate的数值来看模型是否需要context 。结果发现：在输入完整的源文本时，模型并不需要visual context，最终效果提升是因为visual context视作一种radom noise从而实现对模型的正则化。在输入不完整的源文本(比如输入句子有错，有歧义，visual grounded token 被mask)时，visual context还是可以补充不完整的源文本的。
  * 思考：没啥感想，就是觉得研究某种信息是否被模型需要，可以采用一个gate机制，看看以后会不会有类似的问题可以拿来研究。

### 分析

* Lower Perplexity is Not Always Human-Like，ACL2021
  * 就看了个标题，标题说明一切，低的PPL并不总是和人类评测相关







