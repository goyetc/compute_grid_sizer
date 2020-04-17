# Compute Grid Sizing Tool

## Typical workflow:
- based on end user requirements for X cores and Y memory (Xc-Yg), what is the correct node size to use to provide Xc-Yg to Z users? 

## Produce estimates using the following details:

### Inputs
- hw tier resources required
- host/node sizes available (public cloud specific)

### Outputs
--> A list of hardware options, sorted by:
- relative efficiency (8:1 bias, memory:compute)
- number of concurrent runs for Xc-Yg 'hw tier' requirement

### Contents
* [dev notebook] (https://vip.domino.tech/u/goyetc/compute-grid-sizing/view/calculator_dev.ipynb)
* [cg_node_sizer.py] (https://vip.domino.tech/u/goyetc/compute-grid-sizing/view/cg2_node_sizer.py)
* [Launcher] (https://vip.domino.tech/u/goyetc/compute-grid-sizing/endpoints/launchers#/launchers/) 

### Example output
*  (https://vip.domino.tech/u/goyetc/compute-grid-sizing/view/results/node_recommendations_4.0_16.0.html) 

### Example host/node data, AWS:

|Instance   |vCPU*|Mem (GiB)|
|-----------|:-----:|:---------:|
|m5.xlarge  |4    |16       |
|m5.2xlarge |8    |32       |
|m5.4xlarge |16   |64       |
|m5.8xlarge |32   |128      |
|m5.12xlarge|48   |192      |
|m5.16xlarge|64   |256      |
|m5.24xlarge|96   |384      |
|c4.large   |2    |3.75     |
|c4.xlarge  |4    |7.5      |
|c4.2xlarge |8    |15       |
|c4.4xlarge |16   |30       |
|c4.8xlarge |36   |60       |
|c5.large   |2    |4        |
|c5.xlarge  |4    |8        |
|c5.2xlarge |8    |16       |
|c5.4xlarge |16   |32       |
|c5.9xlarge |36   |72       |
|c5.12xlarge|48   |96       |
|c5.18xlarge|72   |144      |
|c5.24xlarge|96   |192      |

---

### to-do
* GPU
* combo sizing (e.g., size for hw tier A and hw tier b concurrently) 
* shiny app
