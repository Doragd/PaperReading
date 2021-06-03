# :memo: Paper Reading

> 2021-6-3: 创建了本仓库
>
> 问渠哪得清如许 为有源头活水来

## :dart: Calendar

* 2021/6

| Mon  | Tue  | Wed  |      Thu       | Fri  | Sat  | Sun  |
| :--: | :--: | :--: | :------------: | :--: | :--: | :--: |
|  31  |  1   |  2   | 3:sweat_drops: |  4   |  5   |  6   |
|  7   |  8   |  9   |       10       |  11  |  12  |  13  |
|  14  |  15  |  16  |       17       |  18  |  19  |  20  |
|  21  |  22  |  23  |       24       |  25  |  26  |  27  |
|  28  |  29  |  30  |       1        |  2   |  3   |  4   |

##  :game_die: Notes

### 数据集

* Figurative Language in Recognizing Textual Entailment，ACL 2021 Findings
  * NLI任务的新数据集，涉及到了明喻识别，暗喻识别和讽刺识别，感觉挺难的，在MNLI上微调的roberta-large表现不太行，尤其是在涉及到需要词汇知识和语用推理的example上面。
  * 思考：没啥感想，看看以后能不能用来测试文本分类，感觉需要引入额外的知识来判断

###  文本摘要

* Demoting the Lead Bias in News Summarization via Alternating Adversarial Learning，ACL2021
  * 抽取式摘要在一些特定领域数据上往往会有一些bias，比如news数据上，一般新闻摘要数据上，靠前的句子一般都是主旨句，也就是可以选取作为summary。不过每个数据集的bias程度并不一样，不能完全依赖这种bias来设计模型，理想中应该按照句子语义来确定。之前的方式就是去shuffle句子，这样会丢失句子之间的联系信息。这篇文章研究的就是如何设计encoder，使得编码的特征能够尽量不包含句子的位置信息，从而使得预测时候对位置信息减少依赖性。但同时，对于一些bias比较重的，严重依赖位置bias的数据集不能性能降太多。否则的话，直接把position embedding去掉不就可以不包含位置信息了吗。这篇的亮点就是设计对抗方式让encoder尽快不包含位置信息，亮点在于多个MLP的使用和与均匀分布的拉近：
  * 典型但是又有些不同的对抗学习：
    1.阶段1.固定预训练摘要模型，训练predictor去预测句子在文档中位置
    2.阶段2..固定predictor，去更新摘要模型使得对抗预测loss最大化。
    注意到：这里实际并不是最大化熵的形式。而是假定当预测不出来时，predictor应该落入一个平凡解，也就是等概率预测每个位置，即预测概率分布是一个均匀分布。所以相当于最小化两个分布之间的距离。
  * 对每个位置的预测都采用相同的MLP会导致位置信息采用其他方式去编码，为了避免这种情况，所以对每个位置分别去用一个MLP去预测，让encoder难以通过其他隐式编码方式来保持句子的位置信息！
  * 思考：可能这种对抗方式可以用来过滤位置信息，不过？位置信息不是可以通过去掉position embedding来去掉吗？

### 多模态

* Good for Misconceived Reasons: An Empirical Revisiting on the Need for Visual Context in Multimodal Machine Translation，ACL2021
  * 多模态机器翻译指在纯文本机器翻译中加入相关的visual context信息来增强翻译效果（两种方式：一种给定源文本和一张相关图片，生成目标文本，一种是给定源文本，去检索一些相关图像，结合起来生成目标文本），实际很多人就在质疑到底需不需要visual context。以前的研究方法是把相关图像替换成随机图像来看效果变化，但实际上这种方式并不能直接看出到底需不需要visual context。这篇文章其实就是提出一个gate机制，把visual context通过一个gate去传入模型，最后检查gate的数值来看模型是否需要context 。结果发现：在输入完整的源文本时，模型并不需要visual context，最终效果提升是因为visual context视作一种radom noise从而实现对模型的正则化。在输入不完整的源文本(比如输入句子有错，有歧义，visual grounded token 被mask)时，visual context还是可以补充不完整的源文本的。
  * 思考：没啥感想，就是觉得研究某种信息是否被模型需要，可以采用一个gate机制，看看以后会不会有类似的问题可以拿来研究。

### 分析

* Lower Perplexity is Not Always Human-Like，ACL2021
  * 就看了个标题，标题说明一切，低的PPL并不总是和人类评测相关







