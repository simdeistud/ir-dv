# Boolean Retrieval IR for the CRAN corpus

## Code and dependencies
The codebase is stored in `/src` while the `requirements.txt` file is in the root directory.

## Application
The application can be started using `python -m src.main` from the project root folder after installing the proper dependencies. When indexing the corpus using the various IR implementations it will produce Pickle files inside `/data` so that subsequent runs don't need to re-index. The IR recognizes capital logical operators such as `AND`, `OR`, `NOT` and supports parenthesis.

## Test suite
Inside `/benchmarks` there is a Jupyter notebook and an exported Markdown version presenting a series of tests of the IR on the Cranfield corpus.

## Disclosure
The code transforming the query to an AST was developed with the help of an LLM.
