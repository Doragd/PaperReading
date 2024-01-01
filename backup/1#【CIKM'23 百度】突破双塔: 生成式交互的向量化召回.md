# 【CIKM'23 百度】突破双塔: 生成式交互的向量化召回

# CIKM'23 百度 | 突破双塔: 生成式交互的向量化召回
* 参考论文：I^3 Retriever: Incorporating Implicit Interaction in Pre-trained Language Models for Passage Retrieval
* 公司：百度
* 链接：https://arxiv.org/pdf/2306.02371.pdf
* Code: https://github.com/Deriq-Qian-Dong/III-Retriever
* 会议：CIKM2023

# 回顾
从dense retrieval任务说起，主要范式有这么几种，一种是双塔（DSSM）、一种是单塔（convKNRM），一种是双塔+迟交互（poly-encoder, colBERT）。这里只列了一些经典工作，具体可以看人大的一篇[survey](https://arxiv.org/pdf/2211.14876.pdf)。

众所周知，单塔采用全交互方式效果好，但是没法适配向量化召回的框架，也就是无法离线建向量索引，需要实时过模型算分数。而双塔虽然能适配该框架，但是无法做到q侧和d侧的细粒度交互，效果弱于单塔。colBERT这类工作则属于是两种框架的结合，具体来说就是双塔过计算图得到token-level的n个向量，q侧每个token向量找到最相似的d侧的token向量，然后相似度求和，即maxSim算子。这种multi-vector indexing的做法实际还是不太适配现有的向量化召回框架，至少没法开箱即用。

![](https://files.mdnice.com/user/47902/b9b0273b-f46e-4853-ba6c-564a917c4a91.png)


回到向量化召回上，如何突破双塔成了一个很好的研究主题。从字节的DR到阿里妈妈的二向箔，再到今年华为的一篇利用VQ和倒排索引来突破双塔的[文章](https://arxiv.org/pdf/2311.18213.pdf)，很多人都做了探索。



但是，最理想的做法是在不额外增加serving成本（架构改造或者索引构建耗时等）的情况下，实现突破双塔，即使可能效果没上述工作这么好，从ROI上说也比较能接受。这种方式的核心在于如何不改变现有框架的前提下，引入交叉特征。一篇比较经典的工作是美团的对偶增强双塔[模型](https://dlp-kdd.github.io/assets/pdf/DLP-KDD_2021_paper_4.pdf)，即在训练时，q侧和d侧各自fake出一段embedding作为底层特征，去学习对方正样本的输出表征。该段特征预期上其实是与对方有过正反馈行为的输出表征的均值。可以看到，经过这种方法处理后的表征，能够携带对方表征的信息，隐式实现了交叉特征的引入。

不过，这种方式引入的交叉特征实际是非常"粗粒度"和"高阶"的，即携带的信息仅仅是对方tower最后输出的表征，对方tower在编码这段表征时，也仅仅只利用了fake的emb和tower本身的输入特征的交互。我们不妨把这种fake过程做得更加"generative"一点。

于是，本文横空出世。

# 方法

![](https://files.mdnice.com/user/47902/4edfce1b-54d1-4cc4-a71c-b49e7e216d70.png)
这篇文章主要是在passage retrieval上做的工作，核心关注是如何提高双塔相关性匹配的效果。具体而言，就是在doc侧设计一个轻量的query生成模块，利用doc侧特征作为输入，去fake一个query侧表征，去重构出query侧的输入特征。这样一来，doc侧也能用生成式的方式去引入另一侧的特征，并从底层开始实现特征交叉。当然这里需要注意的是，也仅仅是在正样本上执行重构loss。

最后效果也是不遑多让，同时serving的效率也和纯双塔持平。

![](https://files.mdnice.com/user/47902/b8d0a883-2aa0-40a6-a03f-d6347fa72706.png)

![](https://files.mdnice.com/user/47902/61b49996-90d5-4580-823a-b0f05dafe6df.png)

除了效果以外，需要关心的一点是，”生成“的fake query特征究竟好不好，究竟能不能重构出对方tower的特征。作者对这一点也做了case study。可以看到生成的fake query有很好的泛化能力，既能命中训练集中对应query的若干term，测试集中也可以泛化出其他的term。

![](https://files.mdnice.com/user/47902/7d50f646-64ae-44c2-bc04-d86d5eb6bdfa.png)

# 进一步思考
这篇工作其实比较类似于doc2query的做法，不过doc2query是离线训一个生成模型来生成多个query作为doc的补充，这里则是一个端到端的做法。一种更暴力的方法则是不用生成式，而直接用离线统计的方式，在doc侧引入一堆和这个doc有相关的query作为扩展。

但是笔者更想强调的是，这种生成式方法其实也可以应用在向量化召回中去引入交叉特征。对偶增强双塔这篇工作珠玉在前，给了我们很多启发。这篇工作则告诉我们，其实我们可以在双塔中用生成式的方法去fake出更多对方的输入特征，而不仅仅限于一段fake对方输出表征的特征。同时，这种的好处是，在输入层就可以引入对方的特征，而后通过DNN则可以做更复杂和更细粒度的交互，而不仅仅限于顶层的内积。

当然，所有一切能work的前提在于fake出来的特征需要学到对方相应特征的语义。这涉及到两方面的问题：

* 怎么设计重构loss和生成模块
* 怎么挑选需要fake的特征

后者，笔者认为更重要，直觉上看，fake泛化特征应该比fake id类特征更容易，对召回而言可能效果也会比较好。同时，笔者也认为，fake的特征可能并不需要学的那么精确，实际所有fake出的特征应该是所有正反馈行为下对方特征的聚类表示。

总之而言，笔者认为这可能也是一种在召回侧引入交叉特征的做法。读者们或者也可以尝试，当然如果本文有任何错漏，也欢迎大家批评指正。




---

* Link: https://github.com/Doragd/PaperReading/issues/1
* Labels: `召回`
* Creation Date: 2024-01-01T13:15:56Z
