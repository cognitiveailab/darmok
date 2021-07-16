Darmok and Jalad at Tanagra: A Dataset and Model for English-Tamarian Translation
=========================================================================

This is the repository for a short, for-fun project in translating the often-discussed metaphorical language of the Children of Tama (Tamarians) from Star Trek: The Next Generation into English. 

Data (Tamarian-English Dictionary)
========
A direct link to the Tamarian-English dictionary can be found [here](dictionary/Tamarian%20Dictionary.tsv).

The Tamarian-English dictionary is provided in both Excel (xlxs) and Tab-Delimied (tsv) formats in [/dictionary/](dictionary/) .

Please note that the inferred meanings of the 20 utterances from the *Darmok* episode are used from this Reddit thread: https://www.reddit.com/r/DaystromInstitute/comments/4ggwo5/the_tamarian_language_an_analysis/


Data (Folds for training model)
========
The train, development, and test crossvalidation folds for training and evaluating the model can be found in [/folds/](folds/)

Results
========
The output predictions of the models are provided in JSONL and TSV format in [/results/](results/)

Pre-trained Models
========
Pre-trained models are available at: ...

Code
========
The T5 model was trained using the Huggingface Transformers library.  This repository has a fork of that library, and made use of a slightly modified translation example (node that the output of this example currently only handles a single GPU and batch size of 1 -- other configurations are not guaranteed to align source and predicted sentences with their scores in the output files correctly).  The example can be found [here](transformers/examples/pytorch/translation/).

Further Reading
========

[Wikipedia: Darmok](https://en.wikipedia.org/wiki/Darmok)

[The Atlantic: Shaka, when the walls fell](https://www.theatlantic.com/entertainment/archive/2014/06/star-trek-tng-and-the-limits-of-language-shaka-when-the-walls-fell/372107/)

[Memory Alpha: The Tamarian Language](https://memory-alpha.fandom.com/wiki/Tamarian_language)


## References

...

