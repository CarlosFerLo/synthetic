# synthetic
Synthetic Cognitions framework for developing language model agents.

## Features
With synthetic we introduce an easy way to work with currently known and used concepts for agents like [functions](#functions) and introduce new ones as [tags](#tags) and [widgets](#tags).

### Functions
The concept of function is well known to coders, but in the case of language model agents it mainly consists of an object that accepts a string as an input and returns one as an output. This kind of function was used in the [ReAct](https://arxiv.org/abs/2210.03629) paper, but synthetic functions are inspired in the ones on the [Toolformer](https://arxiv.org/abs/2302.04761) paper. (For a further explanation of how functions work read the Toolformer article)

Wheras in those cases functions where expected only to return a string, here we will go a step further allowing them to modify the prompt and generated sequence itself. This comes handy when working with [tags](#tags) and [widgets](#widgets).

### Tags
Tags are the main concept that this framework introduces. They are just a wrapper around plain text in the prompt or the generation (we will stop to distinguish them further down), just like HTML tags.

A tag consist of 3 things: identifier, id, content. Here is an example:
    <identifier:id> content </identifier>

Then we can start to make this concept more and more complexity. First we can add [style validators](#validators) for the content of a tag to guarantee the generation of the language model follows the style we thought of for that tag. For example:

    This would work: <no-spaces:id>thisTextHasNoSpaces</no-spaces> 
    This will fail: <no-spaces:id>this text has spaces</no-spaces>

Validators can update tag content when the test fails and can also be run if the tag is closed (for more info go to the [Validators](#validators) section).

// TODO: end README.md

