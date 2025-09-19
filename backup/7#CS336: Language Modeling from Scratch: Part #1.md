# CS336: Language Modeling from Scratch: Part #1

> https://www.bilibili.com/video/BV1YKhhzBE1M

<img width="3442" height="546" alt="Image" src="https://github.com/user-attachments/assets/7cf7bcc7-0147-46fd-a63c-d4ede0080714" />
* 构造一个小的语言模型可能并不具有代表性（<1B的参数），为什么呢

1. 随着参数量的提升，FLOPS的重点从注意力层转移到了FFN，所以如果在小参数量情况下专注优化MHA，这并不能外推到大模型上去，在更大规模下，MHA优化的作用就被稀释了

<img width="3188" height="1508" alt="Image" src="https://github.com/user-attachments/assets/2c7ceb18-43a4-4753-9aa9-e78d5d0d9ac5" />

2. 涌现行为，一定是在FLOPS到达一定地步上，才会出现，比如上下文学习能力，在小模型上如果发现不work，并不意味着语言模型真的不行

<img width="3000" height="1708" alt="Image" src="https://github.com/user-attachments/assets/67450cc5-8e7b-4212-a2e5-727388515f9d" />

这个课程教什么！
* 不但教你transformer是怎么work的，关键还教你去压榨硬件的性能，培养你的规模化思维，以及一些直觉，什么样的数据和建模能够产生好的模型

<img width="3434" height="692" alt="Image" src="https://github.com/user-attachments/assets/b1b8f74f-8a27-4259-b9b1-ba589110865b" />



---

* Link: https://github.com/Doragd/PaperReading/issues/7
* Labels: `课程`
* Creation Date: 2025-09-19T05:43:25Z
