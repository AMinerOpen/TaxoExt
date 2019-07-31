# TaxoExt

Extend taxonomy by labeled documents. In this repo, we extend NSFC 3 level discipline taxonomy by NSFC project keywords.

# Dependencies

* Python 3

# Run

For raw text, you can extract keywords using the same approach in [HierRec](https://github.com/AMinerOpen/HierRec). In this repo, we provide a processed file. Therefore, just:

* download [*data/nsfc_kws_filt.jl*](https://lfs.aminer.cn/misc/awoe/nsfc_kws_filt.zip), which is a temporary file of [HierRec](https://github.com/AMinerOpen/HierRec).
* run *main.py* to get result.

We use [PMI](https://en.wikipedia.org/wiki/Pointwise_mutual_information) to compute the relativeness of a word and a discipline. And the softmax of PMI is used to represent the discipline distribution of a word.
